import csv
import math
from dataclasses import dataclass
from pathlib import Path


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
    def profit_per_labor_hour(self) -> float:
        if self.labor_hours <= 0:
            return 0.0
        return self.net_profit / self.labor_hours

    @property
    def break_even_ears(self) -> int:
        contribution_margin = self.price_per_ear - self.cogs_per_ear
        if contribution_margin <= 0:
            return -1

        fixed_costs = self.vendor_fee + (self.labor_hours * self.hourly_rate) + self.travel_cost
        if fixed_costs <= 0:
            return 0  # Already breaking even at 0 sales if fixed costs are covered/subsidized

        # Add a tiny epsilon to prevent floating-point precision miscalculations in math.ceil
        exact_ears = fixed_costs / contribution_margin
        return math.ceil(exact_ears - 1e-9)


def load_events_from_csv(filepath: str) -> list[EventRecord]:
    events: list[EventRecord] = []
    with open(filepath, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            events.append(
                EventRecord(
                    name=row["name"].strip(),
                    event_type=row["event_type"].strip(),
                    # Using int(float(...)) prevents crashes if CSV exports integers as floats (e.g., "100.0")
                    ears_sold=int(float(row["ears_sold"])),
                    price_per_ear=float(row["price_per_ear"]),
                    vendor_fee=float(row["vendor_fee"]),
                    cogs_per_ear=float(row["cogs_per_ear"]),
                    labor_hours=float(row["labor_hours"]),
                    hourly_rate=float(row["hourly_rate"]),
                    travel_cost=float(row["travel_cost"]),
                )
            )
    return events


def generate_report(events: list[EventRecord]) -> str:
    lines = [
        "=" * 76,
        "MUTHER SHUCKERS COWBOY CORN — EVENT PROFITABILITY REPORT (V2)",
        "=" * 76,
    ]

    sorted_events = sorted(events, key=lambda e: e.net_profit, reverse=True)

    for event in sorted_events:
        if event.net_profit > 0:
            status = "PROFITABLE ✅"
        elif event.net_profit == 0:
            status = "BREAK-EVEN ⚖️"
        else:
            status = "UNPROFITABLE ❌"

        be_display = (
            f"{event.break_even_ears} ears"
            if event.break_even_ears != -1
            else "Impossible (Price <= COGS)"
        )

        lines.append(f"\nEvent: {event.name} ({event.event_type}) — {status}")
        lines.append(f"  Ears Sold: {event.ears_sold} | Break-Even Needed: {be_display}")
        lines.append(f"  Gross Revenue: ${event.gross_revenue:,.2f} | Total Cost: ${event.total_cost:,.2f}")
        lines.append(
            f"  Net Profit: ${event.net_profit:,.2f} ({event.profit_margin:.1f}% margin) | "
            f"Profit/Labor Hr: ${event.profit_per_labor_hour:,.2f}/hr"
        )

    total_net = sum(e.net_profit for e in events)
    winners = [e for e in events if e.net_profit > 0]
    losers = [e for e in events if e.net_profit < 0]

    lines.append("\n" + "=" * 76)
    lines.append(f"SUMMARY: {len(winners)} Profitable Events | {len(losers)} Money-Losing Events")
    lines.append(f"NET PORTFOLIO PROFIT: ${total_net:,.2f}")
    lines.append("=" * 76)

    return "\n".join(lines)


if __name__ == "__main__":
    csv_path = Path(__file__).parent / "events.csv"
    events = load_events_from_csv(str(csv_path))
    report = generate_report(events)
    print(report)

    report_path = Path(__file__).parent / "report.txt"
    report_path.write_text(report, encoding="utf-8")
    print(f"\nSaved report to {report_path}")
