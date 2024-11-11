# utils.py
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def create_tax_comparison_chart(new_regime_tax, old_regime_tax):
    """Create a bar chart comparing tax components between regimes"""
    categories = ['Base Tax', 'Surcharge', 'Cess', 'Total Tax']
    new_values = [new_regime_tax['base_tax'], new_regime_tax['surcharge'], 
                 new_regime_tax['cess'], new_regime_tax['total_tax']]
    old_values = [old_regime_tax['base_tax'], old_regime_tax['surcharge'], 
                 old_regime_tax['cess'], old_regime_tax['total_tax']]
    
    fig = go.Figure(data=[
        go.Bar(name='New Regime', x=categories, y=new_values, marker_color='#0066cc'),
        go.Bar(name='Old Regime', x=categories, y=old_values, marker_color='#006600')
    ])
    
    fig.update_layout(
        title='Tax Comparison Between Regimes',
        barmode='group',
        height=400
    )
    return fig

def create_tax_breakdown_pie(tax_details, regime_type):
    """Create a pie chart showing tax component breakdown"""
    labels = ['Base Tax', 'Surcharge', 'Cess']
    values = [tax_details['base_tax'], tax_details['surcharge'], tax_details['cess']]
    
    colors = ['#0066cc', '#4d94ff', '#99c2ff'] if regime_type == 'New' else ['#006600', '#00b300', '#00ff00']
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, marker_colors=colors)])
    fig.update_layout(
        title=f'{regime_type} Regime Tax Breakdown',
        height=300
    )
    return fig

def create_monthly_savings_chart(annual_savings):
    """Create a line chart showing monthly savings"""
    months = list(range(1, 13))
    monthly_savings = [annual_savings/12 * i for i in months]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=monthly_savings, mode='lines+markers',
                            line=dict(color='#0066cc', width=2)))
    
    fig.update_layout(
        title='Potential Monthly Savings',
        xaxis_title='Month',
        yaxis_title='Cumulative Savings (₹)',
        height=300
    )
    return fig

def get_tax_saving_tips(income, age, current_deductions):
    """Generate personalized tax saving tips"""
    tips = []
    
    max_80c = 150000
    max_80d = 50000 if age >= 60 else 25000
    max_nps = 50000
    
    if current_deductions.get('80C', 0) < max_80c:
        remaining_80c = max_80c - current_deductions.get('80C', 0)
        tips.append(f"You can still invest ₹{remaining_80c:,} under Section 80C (EPF, ELSS, PPF)")
    
    if current_deductions.get('80D', 0) < max_80d:
        remaining_80d = max_80d - current_deductions.get('80D', 0)
        tips.append(f"You can save up to ₹{remaining_80d:,} by paying health insurance premium under Section 80D")
    
    if current_deductions.get('80CCD', 0) < max_nps:
        remaining_nps = max_nps - current_deductions.get('80CCD', 0)
        tips.append(f"Additional tax benefit of up to ₹{remaining_nps:,} available through NPS investment")
    
    return tips

def calculate_advance_tax_schedule(total_tax):
    """Calculate advance tax payment schedule"""
    schedule = [
        {'Due Date': 'June 15, 2024', 'Percentage': '15%', 'Amount': total_tax * 0.15},
        {'Due Date': 'September 15, 2024', 'Percentage': '45%', 'Amount': total_tax * 0.45},
        {'Due Date': 'December 15, 2024', 'Percentage': '75%', 'Amount': total_tax * 0.75},
        {'Due Date': 'March 15, 2025', 'Percentage': '100%', 'Amount': total_tax}
    ]
    return schedule

def create_educational_content():
    """Generate educational content about taxation"""
    return {
        'basic_concepts': {
            'Gross Total Income': 'Sum of all your income sources before any deductions',
            'Taxable Income': 'Income on which tax is actually calculated after all deductions',
            'Tax Liability': 'The total amount of tax you need to pay',
            'Standard Deduction': 'A flat deduction available to all taxpayers under new regime (₹75,000 for FY 2024-25)',
        },
        'deductions_explained': {
            '80C': 'Investments in PPF, EPF, ELSS, Life Insurance Premium, etc.',
            '80D': 'Health Insurance Premium for self, family and parents',
            '80CCD(1B)': 'Additional deduction for NPS contribution',
            'HRA': 'House Rent Allowance exemption for those living in rented accommodation',
        },
        'important_dates': {
            'Advance Tax': ['15 Jun', '15 Sep', '15 Dec', '15 Mar'],
            'Tax Filing': '31 July 2025',
            'Tax Audit': '30 September 2024',
        }
    }