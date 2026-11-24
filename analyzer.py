from dataclasses import dataclass
import math

@dataclass
class EventRecord:
    name: str
    event_type: str       
    ears_sold: int
    price_per_ear: float
    vendor_fee: float
    cogs_per_ear: float   
    labor_hours: float
    hourly_rate: float
    travel_cost: float

    @property
    def gross_revenue(self) -> float:
        return self.ears_sold * self.price_per_ear

    @property
    def total_cost(self) -> float:
        variable_cogs = self.ears_sold * self.cogs_per_ear
        labor_cost = self.labor_hours * self.hourly_rate
        return self.vendor_fee + variable_cogs + labor_cost + self.travel_cost

    @property
    def net_profit(self) -> float:
        return self.gross_revenue - self.total_cost

    @property
    def profit_margin(self) -> float:
        if self.gross_revenue == 0:
            return 0.0
        return (self.net_profit / self.gross_revenue) * 100

    @property
    def break_even_ears(self) -> int:
        contribution_margin = self.price_per_ear - self.cogs_per_ear
        if contribution_margin <= 0:
            return -1
        fixed_costs = self.vendor_fee + (self.labor_hours * self.hourly_rate) + self.travel_cost
        # Use math.ceil so you never underestimate the units needed to cover fixed costs
        return math.ceil(fixed_costs / contribution_margin)


def analyze_events(events: list[EventRecord]) -> None:
    print("=" * 72)
    print("MUTHER SHUCKERS COWBOY CORN — EVENT PROFITABILITY REPORT")
    print("=" * 72)

    sorted_events = sorted(events, key=lambda e: e.net_profit, reverse=True)

    for event in sorted_events:
        if event.net_profit > 0:
            status = "PROFITABLE ✅"
        elif event.net_profit == 0:
            status = "BREAK-EVEN ⚖️"
        else:
            status = "UNPROFITABLE ❌"
            
        print(f"\nEvent: {event.name} ({event.event_type}) — {status}")
        print(f"  Ears Sold: {event.ears_sold} | Break-Even Needed: {event.break_even_ears} ears")
        print(f"  Gross Revenue: ${event.gross_revenue:,.2f} | Total Cost: ${event.total_cost:,.2f}")
        print(f"  Net Profit: ${event.net_profit:,.2f} ({event.profit_margin:.1f}% margin)")

    total_net = sum(e.net_profit for e in events)
    winners = [e for e in events if e.net_profit > 0]
    losers = [e for e in events if e.net_profit < 0]

    print("\n" + "=" * 72)
    print(f"SUMMARY: {len(winners)} Profitable Events | {len(losers)} Money-Losing Events")
    print(f"NET PORTFOLIO PROFIT: ${total_net:,.2f}")
    print("=" * 72)


if __name__ == "__main__":
    sample_events = [
        EventRecord("Destin Seafood Festival", "Major Festival", 620, 7.00, 850.00, 1.35, 16, 15.00, 60.00),
        EventRecord("Crestview Saturday Market", "Local Market", 95, 7.00, 150.00, 1.35, 8, 15.00, 25.00),
        EventRecord("Fort Walton Beach Pop-Up", "Weekday Pop-Up", 55, 7.00, 100.00, 1.35, 7, 15.00, 40.00),
        EventRecord("30A Spring Concert Series", "Peak Event", 410, 8.00, 500.00, 1.40, 12, 15.00, 50.00),
    ]
    analyze_events(sample_events)
