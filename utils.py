import numpy as np

def calculate_total_cost(square_feet, quality_level):
    """Calculate total costs based on square footage and quality level in AED."""
    base_costs_aed = {
        'basic': 300,    # AED per sq ft
        'medium': 380,
        'luxury': 780
    }
    return square_feet * base_costs_aed[quality_level]

def calculate_dubai_fees(property_value):
    """Calculate Dubai property related fees."""
    dld_fee = property_value * 0.04  # 4% Dubai Land Department fee
    broker_fee = property_value * 0.02  # 2% broker fee
    title_deed_fee = 430  # Fixed amount
    conveyance_fee = 7350  # Fixed amount

    total_fees = dld_fee + broker_fee + title_deed_fee + conveyance_fee

    return {
        'dld_fee': dld_fee,
        'broker_fee': broker_fee,
        'title_deed_fee': title_deed_fee,
        'conveyance_fee': conveyance_fee,
        'total_fees': total_fees
    }

def estimate_property_values(initial_value, total_cost, market_factor):
    """Estimate property values after renovation with different markup scenarios."""
    value_increase = total_cost * (1 + market_factor)
    base_value = initial_value + value_increase

    return {
        'conservative': base_value * (1.15 + market_factor),  # +15% plus market factor
        'moderate': base_value * (1.25 + market_factor),      # +25% plus market factor
        'optimistic': base_value * (1.35 + market_factor)     # +35% plus market factor
    }

def calculate_roi_with_split(initial_investment, final_value, total_cost, holding_period):
    """Calculate ROI and profit split between investor and company."""
    total_investment = initial_investment + total_cost
    profit = final_value - total_investment

    # Split profit: 88% investor, 12% company
    investor_profit = profit * 0.88
    company_profit = profit * 0.12

    # Calculate annual ROI based on investor's portion
    annual_roi = (investor_profit / total_investment) * (12 / holding_period) * 100

    return {
        'total_profit': profit,
        'investor_profit': investor_profit,
        'company_profit': company_profit,
        'annual_roi': annual_roi
    }

def calculate_share_investment(total_investment, share_amount, holding_period):
    """Calculate share-based investment returns."""
    share_percentage = (share_amount / total_investment) * 100
    monthly_return_rate = 0.005  # 0.5% per month
    monthly_returns = share_amount * monthly_return_rate
    total_returns = monthly_returns * holding_period

    return {
        'share_percentage': share_percentage,
        'monthly_returns': monthly_returns,
        'total_returns': total_returns,
        'effective_annual_return': monthly_return_rate * 12 * 100  # Convert to annual percentage
    }

def generate_monthly_projection(initial_value, final_value, months):
    """Generate monthly value projections."""
    return np.linspace(initial_value, final_value, months)