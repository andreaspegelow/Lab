PRICE_BASE_AMOUNT: int = 58_800
MAX_PAY_PAR_DAY: int = 1250
COMPENSATION_RATE = 0.7922
WEEKS_PER_MONTH = 4.286
TAX_RATE = 0.30


def calculate_parental_benefit(
    yearly_income_p1: int, yearly_income_p2: int, days_per_week_p1: int, days_per_week_p2: int
):

    assert 0 <= days_per_week_p1 <= 7, "A week has 7 days"
    assert 0 <= days_per_week_p2 <= 7, "A week has 7 days"

    def calculate_daily_compensation(yearly_income):
        return min(yearly_income / 12 / 31 * COMPENSATION_RATE, MAX_PAY_PAR_DAY)

    pay_per_day_p1 = calculate_daily_compensation(yearly_income_p1)
    pay_per_day_p2 = calculate_daily_compensation(yearly_income_p2)

    monthly_benefit_p1 = pay_per_day_p1 * days_per_week_p1 * WEEKS_PER_MONTH
    monthly_benefit_p2 = pay_per_day_p2 * days_per_week_p2 * WEEKS_PER_MONTH
    total_benefit = monthly_benefit_p1 + monthly_benefit_p2

    after_tax_p1 = monthly_benefit_p1 * (1 - TAX_RATE)
    after_tax_p2 = monthly_benefit_p2 * (1 - TAX_RATE)
    total_after_tax = total_benefit * (1 - TAX_RATE)

    return f"\nParent 1 Monthly Benefit: {monthly_benefit_p1:.2f} SEK (After Tax: {after_tax_p1:.2f} SEK)\n" \
           f"Parent 2 Monthly Benefit: {monthly_benefit_p2:.2f} SEK (After Tax: {after_tax_p2:.2f} SEK)\n" \
           f"Total Monthly Benefit: {total_benefit:.2f} SEK (After Tax: {total_after_tax:.2f} SEK)\n"


print(calculate_parental_benefit(684000, 504000, 1, 1))
