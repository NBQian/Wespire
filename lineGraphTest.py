import random
from datetime import date, timedelta
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

products = [{'Date': '1997-10-02', 'Mode': 'CPF-OA (Yearly)', 'SinglePaymentAmount': 0, 'YearlyPaymentAmount': 4509.0, 'PaymentEndDate': '2033-10-02', 'PremiumPayoutMode': None, 'PremiumPayoutYear': None, 'PremiumPayoutEndYear': None, 'PremiumPayoutAmount': None},
             {'Date': '1997-10-02','Mode': 'Cash (Single)', 'SinglePaymentAmount': 4005.99, 'YearlyPaymentAmount': 0.0, 'PaymentEndDate': '2033-08-15', 'PremiumPayoutMode': None, 'PremiumPayoutYear': None, 'PremiumPayoutEndYear': None, 'PremiumPayoutAmount': None}, {'Date': '2013-10-02','Mode': 'Cash (Monthly)', 'SinglePaymentAmount': 0, 'YearlyPaymentAmount': 3407.99, 'PaymentEndDate': '2049-01-11', 'PremiumPayoutMode': 'Yearly', 'PremiumPayoutYear': '2027', 'PremiumPayoutEndYear': '2037', 'PremiumPayoutAmount': 44853.24}]

date_of_birth = datetime(1990, 1, 1)  # Example date of birth

# Define a function to calculate annual payments
def calculate_annual_payments(products, start_age, end_age, dob):
    annual_payments = {age: 0 for age in range(start_age, end_age + 1)}
    current_year = datetime.now().year
    
    for product in products:
        start_date = datetime.strptime(product['Date'], '%Y-%m-%d')
        end_date = datetime.strptime(product['PaymentEndDate'], '%Y-%m-%d')
        mode = product['Mode']
        single_payment_amount = product['SinglePaymentAmount']
        yearly_payment_amount = product['YearlyPaymentAmount']

        if "Single" in mode:
            payment_year = start_date.year
            age_at_payment = payment_year - dob.year
            if start_age <= age_at_payment <= end_age:
                annual_payments[age_at_payment] += single_payment_amount
        else:
            for year in range(start_date.year, end_date.year + 1):
                age_at_year = year - dob.year
                if start_age <= age_at_year <= end_age:
                    if "Monthly" in mode:
                        # Monthly payments, so multiply by 12 to get yearly equivalent
                        annual_payments[age_at_year] += yearly_payment_amount * 12
                    elif "Yearly" in mode:
                        annual_payments[age_at_year] += yearly_payment_amount
                        
    return annual_payments

# Calculate payments from age 20 to 100
start_age = 20
end_age = 100
annual_payments = calculate_annual_payments(products, start_age, end_age, date_of_birth)

df_annual_payments = pd.DataFrame(list(annual_payments.items()), columns=['Age', 'Annual Payment'])
ax = df_annual_payments.plot(kind='line', x='Age', y='Annual Payment', marker='o', linestyle='-', color='#293486', markersize=3.5, figsize=(10, 6))  # Adjust markersize as needed

# Customizing the plot
ax.set_xlabel("Age", fontsize=14, labelpad=20)
ax.set_ylabel("Annual Payment (S$)", fontsize=14, labelpad=20)
plt.xticks(range(start_age, end_age + 1, 10))
plt.legend(['Annual Payment'], fontsize=12)

# Adjusting tick parameters as per the new requirements
ax.tick_params(axis='x', labelsize=13, pad=13)
ax.tick_params(axis='y', labelsize=12, pad=13)

# Setting the title with custom font size, font name, font weight, and padding
ax.set_title('Annual Payment Outflow', fontsize=20, fontname='Arial', fontweight='bold', pad=25)

# Remove grid
ax.grid(False)

# Remove top and right border lines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Before showing the plot, save it to a file
plt.savefig('payment.png', dpi=300, bbox_inches='tight')

def calculate_premium_payouts(products, start_age, end_age, dob):
    premium_payouts = {age: 0 for age in range(start_age, end_age + 1)}
    for product in products:
        if product['PremiumPayoutMode'] == 'Single':
            payout_year = int(product['PremiumPayoutEndYear'])
            payout_age = payout_year - dob.year
            if start_age <= payout_age <= end_age:
                premium_payouts[payout_age] += product['PremiumPayoutAmount']
        elif product['PremiumPayoutMode'] == 'Yearly':
            start_year = int(product['PremiumPayoutYear'])
            end_year = int(product['PremiumPayoutEndYear'])
            for year in range(start_year, end_year + 1):
                age = year - dob.year
                if start_age <= age <= end_age:
                    premium_payouts[age] += product['PremiumPayoutAmount']
    return premium_payouts

# Calculate premium payouts
premium_payouts = calculate_premium_payouts(products, 20, 100, date_of_birth)

# Convert to DataFrame
df_premium_payouts = pd.DataFrame(list(premium_payouts.items()), columns=['Age', 'Premium Payout'])

# Plot
ax = df_premium_payouts.plot(kind='line', x='Age', y='Premium Payout', color='#293486', marker='o', linestyle='-', markersize=3.5, figsize=(10, 6))
ax.set_xlabel("Age", fontsize=14, labelpad=20)
ax.set_ylabel("Premium Payout (S$)", fontsize=14, labelpad=20)
plt.xticks(range(20, 101, 10))
ax.tick_params(axis='x', labelsize=13, pad=13)
ax.tick_params(axis='y', labelsize=12, pad=10)
ax.set_title('Premium Payout Flow', fontsize=20, fontname='Arial', fontweight='bold', pad=25)
ax.grid(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.legend(['Premium Payout'])

# Save the graph as a PNG image
plt.savefig('premium.png', dpi=300, bbox_inches='tight')