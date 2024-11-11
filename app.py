 # app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from utils import *

# Set page configuration
st.set_page_config(
    page_title="Indian Tax Calculator 2024-25",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .big-font {
        font-size:24px !important;
        font-weight: bold;
    }
    .medium-font {
        font-size:20px !important;
    }
    .highlight {
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .tax-result {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 10px 0;
    }
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted #ccc;
        cursor: help;
    }
    .chart-container {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .interactive-element {
        transition: all 0.3s ease;
    }
    .interactive-element:hover {
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

def calculate_capital_gains_tax(ltcg_by_quarter, stcg_by_quarter):
    """Calculate tax for capital gains quarter-wise"""
    total_ltcg = sum(ltcg_by_quarter.values())
    total_stcg = sum(stcg_by_quarter.values())
    
    # LTCG calculation (12.5% after 1.25L exemption)
    ltcg_exemption = 125000
    taxable_ltcg = max(0, total_ltcg - ltcg_exemption)
    ltcg_tax = taxable_ltcg * 0.125
    
    # STCG calculation (20%)
    stcg_tax = total_stcg * 0.20
    
    # Calculate quarter-wise breakdown
    quarterly_tax = {}
    for quarter in ltcg_by_quarter.keys():
        quarter_ltcg = ltcg_by_quarter[quarter]
        quarter_stcg = stcg_by_quarter[quarter]
        
        # Calculate LTCG tax for this quarter
        if total_ltcg > ltcg_exemption:
            quarter_ltcg_tax = (quarter_ltcg / total_ltcg) * ltcg_tax
        else:
            quarter_ltcg_tax = 0
            
        quarter_stcg_tax = quarter_stcg * 0.20
        
        quarterly_tax[quarter] = {
            'ltcg_tax': quarter_ltcg_tax,
            'stcg_tax': quarter_stcg_tax,
            'total': quarter_ltcg_tax + quarter_stcg_tax
        }
    
    return {
        'ltcg_tax': ltcg_tax,
        'stcg_tax': stcg_tax,
        'total_cg_tax': ltcg_tax + stcg_tax,
        'taxable_ltcg': taxable_ltcg,
        'quarterly_tax': quarterly_tax
    }

def calculate_advance_tax_schedule(total_tax, cg_tax_by_quarter):
    """Calculate quarterly advance tax requirements"""
    quarters = {
        "Q1": {"due": "June 15, 2024", "percentage": 15},
        "Q2": {"due": "September 15, 2024", "percentage": 45},
        "Q3": {"due": "December 15, 2024", "percentage": 75},
        "Q4": {"due": "March 15, 2025", "percentage": 100}
    }
    
    regular_tax = total_tax - sum(cg_tax_by_quarter.values())
    cumulative_tax = 0
    schedule = []
    prev_percentage = 0
    
    for q, info in quarters.items():
        # Calculate regular tax for this installment
        regular_tax_due = (regular_tax * info['percentage'] / 100) - cumulative_tax
        
        # Add capital gains tax for this quarter
        cg_tax_due = cg_tax_by_quarter.get(q, 0)
        
        total_due = regular_tax_due + cg_tax_due
        cumulative_tax += regular_tax_due
        
        schedule.append({
            'due_date': info['due'],
            'percentage': info['percentage'],
            'installment_percentage': info['percentage'] - prev_percentage,
            'regular_tax': regular_tax_due,
            'capital_gains_tax': cg_tax_due,
            'total_amount': total_due
        })
        prev_percentage = info['percentage']
    
    return schedule

# Your existing tax calculation functions remain the same
def calculate_tax_new_regime(annual_income):
    standard_deduction = 75000
    taxable_income = annual_income - standard_deduction
    
    tax = 0
    if taxable_income <= 300000:
        tax = 0
    elif taxable_income <= 600000:
        tax = (taxable_income - 300000) * 0.05
    elif taxable_income <= 900000:
        tax = 15000 + (taxable_income - 600000) * 0.10
    elif taxable_income <= 1200000:
        tax = 45000 + (taxable_income - 900000) * 0.15
    elif taxable_income <= 1500000:
        tax = 90000 + (taxable_income - 1200000) * 0.20
    else:
        tax = 150000 + (taxable_income - 1500000) * 0.30
        
    surcharge = 0
    if taxable_income > 50000000:
        surcharge = tax * 0.25
    elif taxable_income > 20000000:
        surcharge = tax * 0.15
    elif taxable_income > 10000000:
        surcharge = tax * 0.10
        
    cess = (tax + surcharge) * 0.04
    
    return {
        'base_tax': tax,
        'surcharge': surcharge,
        'cess': cess,
        'total_tax': tax + surcharge + cess,
        'taxable_income': taxable_income
    }

def calculate_tax_old_regime(annual_income, deductions):
    taxable_income = annual_income - deductions
    
    tax = 0
    if taxable_income <= 250000:
        tax = 0
    elif taxable_income <= 500000:
        tax = (taxable_income - 250000) * 0.05
    elif taxable_income <= 1000000:
        tax = 12500 + (taxable_income - 500000) * 0.20
    else:
        tax = 112500 + (taxable_income - 1000000) * 0.30
        
    surcharge = 0
    if taxable_income > 50000000:
        surcharge = tax * 0.37
    elif taxable_income > 20000000:
        surcharge = tax * 0.25
    elif taxable_income > 10000000:
        surcharge = tax * 0.15
        
    cess = (tax + surcharge) * 0.04
    
    return {
        'base_tax': tax,
        'surcharge': surcharge,
        'cess': cess,
        'total_tax': tax + surcharge + cess,
        'taxable_income': taxable_income
    }

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", 
    ["Tax Calculator", "Educational Center", "Tax Planning", "Help & Support"])

if page == "Tax Calculator":
    st.title("🇮🇳 Income Tax Calculator 2024-25")
    st.markdown("**Developed by Rajesh Parikh**")  
    income_tab, cg_tab = st.tabs(["Regular Income", "Capital Gains"])
    
    with income_tab:
        col1, col2, col3 = st.columns([2,1,1])
        with col1:
            annual_income = st.number_input(
                "Annual Income (₹)",
                min_value=0,
                value=500000,
                step=10000,
                format="%d"
            )
        with col2:
            age = st.number_input("Age", min_value=18, max_value=100, value=35)
        with col3:
            assessment_year = st.selectbox(
                "Assessment Year",
                ["2024-25", "2025-26"],
                index=0
            )

        with st.expander("📝 Deductions Calculator", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                d_80c = st.number_input(
                    "80C Investments",
                    min_value=0,
                    max_value=150000,
                    value=0,
                    help="EPF, PPF, ELSS, etc."
                )
                d_80d = st.number_input(
                    "Health Insurance (80D)",
                    min_value=0,
                    max_value=100000,
                    value=0
                )
            with col2:
                d_80ccd = st.number_input(
                    "NPS Contribution (80CCD)",
                    min_value=0,
                    max_value=50000,
                    value=0
                )
                d_others = st.number_input(
                    "Other Deductions",
                    min_value=0,
                    value=0
                )

            total_deductions = d_80c + d_80d + d_80ccd + d_others
            st.metric(
                "Total Deductions",
                f"₹{total_deductions:,}",
                delta=f"₹{150000-d_80c:,} more possible in 80C",
                delta_color="normal"
            )

    with cg_tab:
        st.subheader("Capital Gains Details (Quarter-wise)")
        
        quarters = {
            "Q1": {"name": "Q1 (Apr-Jun)", "due": "June 15, 2024"},
            "Q2": {"name": "Q2 (Jul-Sep)", "due": "September 15, 2024"},
            "Q3": {"name": "Q3 (Oct-Dec)", "due": "December 15, 2024"},
            "Q4": {"name": "Q4 (Jan-Mar)", "due": "March 15, 2025"}
        }
        
        ltcg_by_quarter = {}
        stcg_by_quarter = {}
        
        for q, info in quarters.items():
            st.write(f"\n### {info['name']} - Due: {info['due']}")
            col1, col2 = st.columns(2)
            with col1:
                ltcg_by_quarter[q] = st.number_input(
                    f"Long Term Capital Gains for {info['name']}",
                    min_value=0,
                    value=0,
                    key=f"ltcg_{q}"
                )
                if q == "Q1":
                    st.caption("Note: First ₹1.25 Lakhs exempt for LTCG (annual)")
            
            with col2:
                stcg_by_quarter[q] = st.number_input(
                    f"Short Term Capital Gains for {info['name']}",
                    min_value=0,
                    value=0,
                    key=f"stcg_{q}"
                )
# Calculate and show results
    if st.button("Calculate Tax 🧮", use_container_width=True):
        # Calculate regular income tax
        new_regime_tax = calculate_tax_new_regime(annual_income)
        old_regime_tax = calculate_tax_old_regime(annual_income, total_deductions)
        
        # Calculate capital gains tax quarter-wise
        cg_tax = calculate_capital_gains_tax(ltcg_by_quarter, stcg_by_quarter)
        
        # Add total capital gains tax to total tax
        new_regime_tax['total_tax'] += cg_tax['total_cg_tax']
        old_regime_tax['total_tax'] += cg_tax['total_cg_tax']
        
        # Display comparative visualizations
        st.subheader("📊 Tax Analysis")
        
        # Display tax comparison chart
        st.plotly_chart(
            create_tax_comparison_chart(new_regime_tax, old_regime_tax),
            use_container_width=True
        )
        
        # Display regime-wise breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### New Tax Regime")
            st.markdown(f"""
            - Taxable Income: ₹{new_regime_tax['taxable_income']:,.2f}
            - Base Tax: ₹{new_regime_tax['base_tax']:,.2f}
            - Surcharge: ₹{new_regime_tax['surcharge']:,.2f}
            - Cess: ₹{new_regime_tax['cess']:,.2f}
            - **Total Tax: ₹{new_regime_tax['total_tax']:,.2f}**
            """)
            
            st.plotly_chart(
                create_tax_breakdown_pie(new_regime_tax, 'New'),
                use_container_width=True
            )
        
        with col2:
            st.markdown("### Old Tax Regime")
            st.markdown(f"""
            - Taxable Income: ₹{old_regime_tax['taxable_income']:,.2f}
            - Base Tax: ₹{old_regime_tax['base_tax']:,.2f}
            - Surcharge: ₹{old_regime_tax['surcharge']:,.2f}
            - Cess: ₹{old_regime_tax['cess']:,.2f}
            - **Total Tax: ₹{old_regime_tax['total_tax']:,.2f}**
            """)
            
            st.plotly_chart(
                create_tax_breakdown_pie(old_regime_tax, 'Old'),
                use_container_width=True
            )

        # Show capital gains breakdown if applicable
        total_ltcg = sum(ltcg_by_quarter.values())
        total_stcg = sum(stcg_by_quarter.values())
        
        if total_ltcg > 0 or total_stcg > 0:
            st.subheader("Capital Gains Tax Breakdown (Quarter-wise)")
            
            # Overall summary
            st.markdown("### Annual Summary")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Long Term Capital Gains**")
                st.write(f"Total LTCG: ₹{total_ltcg:,.2f}")
                st.write(f"Exemption: ₹{125000:,.2f}")
                st.write(f"Taxable LTCG: ₹{cg_tax['taxable_ltcg']:,.2f}")
                st.write(f"LTCG Tax (12.5%): ₹{cg_tax['ltcg_tax']:,.2f}")
            
            with col2:
                st.markdown("**Short Term Capital Gains**")
                st.write(f"Total STCG: ₹{total_stcg:,.2f}")
                st.write(f"STCG Tax (20%): ₹{cg_tax['stcg_tax']:,.2f}")
            
            st.markdown(f"**Total Capital Gains Tax: ₹{cg_tax['total_cg_tax']:,.2f}**")
            
            # Quarter-wise breakdown
            st.markdown("### Quarterly Breakdown")
            
            quarter_cols = st.columns(4)
            for i, (q, info) in enumerate(quarters.items()):
                with quarter_cols[i]:
                    st.markdown(f"**{info['name']}**")
                    qt = cg_tax['quarterly_tax'][q]
                    st.write(f"LTCG: ₹{ltcg_by_quarter[q]:,.2f}")
                    st.write(f"STCG: ₹{stcg_by_quarter[q]:,.2f}")
                    st.write(f"Tax: ₹{qt['total']:,.2f}")

        # Display advance tax schedule
        st.subheader("📅 Advance Tax Schedule")
        
        # Prepare quarterly capital gains tax
        cg_tax_by_quarter = {q: tax['total'] for q, tax in cg_tax['quarterly_tax'].items()}
        schedule = calculate_advance_tax_schedule(new_regime_tax['total_tax'], cg_tax_by_quarter)
        
        # Create advanced tax table
        tax_table = []
        for entry in schedule:
            tax_table.append({
                'Due Date': entry['due_date'],
                'Regular Tax (₹)': f"{entry['regular_tax']:,.2f}",
                'Capital Gains Tax (₹)': f"{entry['capital_gains_tax']:,.2f}",
                'Total Amount (₹)': f"{entry['total_amount']:,.2f}",
                'Cumulative %': f"{entry['percentage']}%"
            })
        
        st.table(pd.DataFrame(tax_table))
            
        st.info("""
        💡 Advance Tax Payment Notes:
        - Regular income tax should be paid as per the cumulative percentages
        - Capital gains tax should be paid in the quarter in which the gains are realized
        - Quarterly dues are cumulative - each installment includes previous quarters
        """)
            
        # Show tax saving recommendation
        tax_diff = abs(new_regime_tax['total_tax'] - old_regime_tax['total_tax'])
        if new_regime_tax['total_tax'] < old_regime_tax['total_tax']:
            st.success(f"💡 Recommendation: Choose **New Tax Regime**\nYou will save ₹{tax_diff:,.2f}")
        else:
            st.success(f"💡 Recommendation: Choose **Old Tax Regime**\nYou will save ₹{tax_diff:,.2f}")

elif page == "Educational Center":
    st.title("📚 Tax Education Center")
    
    selected_topic = st.selectbox(
        "Choose a topic to learn about:",
        ["Basic Tax Concepts", "Deductions & Exemptions", "Tax Saving Investments", "Filing Process"]
    )
    
    educational_content = create_educational_content()
    
    if selected_topic == "Basic Tax Concepts":
        for concept, explanation in educational_content['basic_concepts'].items():
            with st.expander(concept):
                st.write(explanation)
                
    with st.expander("📝 Test Your Knowledge"):
        st.write("Quick Quiz")
        q1 = st.radio(
            "What is the standard deduction under new tax regime?",
            ["₹50,000", "₹75,000", "₹1,00,000"]
        )
        if q1:
            if q1 == "₹75,000":
                st.success("Correct! The standard deduction is ₹75,000 under new tax regime.")
            else:
                st.error("Incorrect. The standard deduction is ₹75,000 under new tax regime.")

elif page == "Tax Planning":
    st.title("🎯 Tax Planning Assistant")
    
    income = st.number_input("Expected Annual Income", value=500000)
    current_investments = st.number_input("Current Tax Saving Investments", value=0)
    
    tips = get_tax_saving_tips(
        income,
        age=35,
        current_deductions={'80C': current_investments}
    )
    
    st.subheader("💡 Personalized Tax Saving Tips")
    for tip in tips:
        st.info(tip)

else:  # Help & Support
    st.title("❓ Help & Support Center")
    
    with st.expander("Frequently Asked Questions"):
        st.subheader("Common Questions")
        questions = {
            "What is the difference between old and new tax regime?": 
                "The new tax regime offers lower tax rates but fewer deductions...",
            "How do I choose between tax regimes?":
                "Consider your total deductions and exemptions...",
            "When should I pay advance tax?":
                "If your tax liability exceeds ₹10,000 in a financial year..."
        }
        for q, a in questions.items():
            st.write(f"**Q: {q}**")
            st.write(f"A: {a}")
    
    st.subheader("📞 Need More Help?")
    issue_type = st.selectbox(
        "What kind of help do you need?",
        ["Calculator Usage", "Tax Rules", "Technical Support", "Other"]
    )
    user_query = st.text_area("Describe your issue")
    if st.button("Submit"):
        st.success("Thanks for reaching out! This is a demo application.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>💡 This calculator is for educational purposes only. Please consult a tax professional for advice.</p>
        <p>Developed by Rajesh Parikh</p>
        <p>Last updated: March 2024</p>
    </div>
""", unsafe_allow_html=True)
