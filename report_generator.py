from fpdf import FPDF
import os

class TradeReport(FPDF):
    def header(self):
        self.set_font("Arial", size=12)
        self.cell(200, 10, "Stock Trading Pre-Trade Report", ln=True, align="C")
    
    def add_decision(self, report):
        self.set_font("Arial", size=10)
        self.multi_cell(0, 10, f"""
        Timestamp: {report['timestamp']}
        Trend: {report['trend']}
        News Sentiment: {report['news_sentiment']}
        Decision: {report['decision']}
        Justification: {report['justification']}
        """)
    
def generate_trade_report(report):
    pdf = TradeReport()
    pdf.add_page()
    pdf.add_decision(report)
    
    # Save the report
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/trade_report_{report['timestamp'].replace(':', '-')}.pdf"
    pdf.output(filename)
    print(f"✅ Report saved to {filename}")

# Example usage
if __name__ == "__main__":
    decision_report = {
        "timestamp": "2025-03-09T12:34:56",
        "trend": "upward",
        "news_sentiment": "positive",
        "decision": "BUY",
        "justification": "The trend is upward and the sentiment is positive. Action: BUY."
    }
    generate_trade_report(decision_report)