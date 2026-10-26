---
layout: post
title: "Valuation Basics: Understanding P/E, P/B, P/S, and Key Balance Sheet Ratios (With Examples)"
date: 2026-10-25
categories: [Finance, Investing]
tags: [Valuation, Fundamental Analysis, Balance Sheet, PE Ratio, PB Ratio, Beginner Guide]
---

If a house is listed for $500,000, you wouldn't know whether it's a good deal just by looking at that price tag. You would immediately ask a few follow-up questions:
- *How much rental income does it produce every month?*
- *What is the land and building actually worth if sold today?*

Stock prices work the exact same way. If Stock A trades at $20 and Stock B trades at $200, Stock A is not automatically "cheaper" than Stock B. You have to compare the price to what the company actually earns and owns.

To do this, investors use **valuation ratios**—most commonly called **"Price-to..." ratios**. 

In this guide, we'll break down the most popular valuation multiples—**Price-to-Earnings (P/E)**, **Price-to-Sales (P/S)**, **Price-to-Book (P/B)**, and other balance sheet ratios—using simple, real-world examples.

<!--more-->

---

## The Big Picture: Income Statement vs. Balance Sheet

A business reports its numbers through two primary financial reports:

1. **The Income Statement:** Measures what the company *earned* over the past year (Sales $\rightarrow$ Profits).
2. **The Balance Sheet:** Measures what the company *owns* and *owes* at this exact moment (Assets $-$ Debts $=$ Net Worth).

```
┌────────────────────────────────────────────────────────────────────────┐
│                        MARKET PRICE PER SHARE (P)                      │
│                What you have to pay in the stock market                │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
       ┌────────────────────────────┴────────────────────────────┐
       │                                                         │
       ▼                                                         ▼
┌──────────────────────────────┐          ┌──────────────────────────────┐
│       INCOME STATEMENT       │          │        BALANCE SHEET         │
│   (What the business earns)  │          │   (What the business owns)   │
├──────────────────────────────┤          ├──────────────────────────────┤
│ • Sales (Revenue) ──► P/S    │          │ • Book Value (Equity)──► P/B │
│ • Net Profit (EPS)──► P/E    │          │ • Cash & Equiv.   ──► P/Cash │
│                              │          │ • Working Capital ──► P/NWC  │
└──────────────────────────────┘          └──────────────────────────────┘
```

---

## 1. Price-to-Earnings (P/E) — "Paying for Profit"

The **Price-to-Earnings** ratio is the most widely quoted stock metric in the world. It tells you how many dollars you are paying for every $1 of annual profit the company generates.

### The Formula

$$\text{P/E Ratio} = \frac{\text{Stock Price}}{\text{Earnings Per Share (EPS)}}$$

$$\text{Earnings Per Share (EPS)} = \frac{\text{Total Annual Net Profit}}{\text{Total Shares Outstanding}}$$

### ☕ Real-World Example

Imagine **Main Street Coffee Co.** has:
- Stock Price: **$40** per share
- Total Annual Net Profit: $2,000,000
- Total Shares: 1,000,000 shares
- **EPS:** $\$2,000,000 / 1,000,000 = \mathbf{\$2}$ per share

$$\text{P/E} = \frac{\$40}{\$2} = \mathbf{20\times}$$

**What this means:**
- You are paying **$20 for every $1 of annual earnings**.
- At the current profit rate, it would take **20 years** of earnings to cover your purchase price.
- The inverse of P/E is the **Earnings Yield**: $\$2 / \$40 = 5\%$. You are effectively earning a $5\%$ return on your investment if all profits were paid out to you.

### How to Interpret P/E
- **Low P/E (e.g., 8–12×):** Often indicates a mature, slow-growing, or higher-risk company (like a utility, bank, or traditional automaker).
- **Average P/E (e.g., 15–22×):** Typical for standard, stable businesses in the broader market (like the S&P 500 average).
- **High P/E (e.g., 30–60×+):** Investors expect the company's profits to grow dramatically in the future (like tech or high-growth healthcare).

---

## 2. Price-to-Sales (P/S) — "Paying for Revenue"

Sometimes a company is growing quickly, but it spends all its money on marketing, hiring, and research, so its net profit is zero or negative. When earnings are zero ($EPS \le 0$), you cannot calculate a P/E ratio.

That's where **Price-to-Sales (P/S)** (also called Price-to-Revenue) comes in. It compares the stock price to the top-line sales before any expenses are subtracted.

### The Formula

$$\text{P/S Ratio} = \frac{\text{Stock Price}}{\text{Sales Per Share}} = \frac{\text{Market Capitalization}}{\text{Total Annual Revenue}}$$

*(Note: In finance, "Sales" and "Revenue" mean the exact same thing—the total money brought in from customers).*

### 💻 Real-World Example

**CloudScale Software** is a young cloud computing startup:
- Stock Price: **$30**
- Market Cap: **$300 Million** (10 million shares $\times$ $30$)
- Annual Revenue: **$100 Million**
- Net Profit: **-$10 Million** (losing money due to heavy expansion)

Because profit is negative, P/E doesn't work. But we can calculate P/S:

$$\text{P/S} = \frac{\text{Market Cap}}{\text{Total Revenue}} = \frac{\$300\text{M}}{\$100\text{M}} = \mathbf{3\times}$$

**What this means:** You are paying **$3 for every $1 of revenue** the company generates.

### The Watch-Out: Gross Margins Matter!
A dollar of revenue in software is very different from a dollar of revenue in retail:
- **Software Company:** Spends $20 to deliver $100 of software (**80% gross margin**). Plenty of room for future profits.
- **Grocery Store:** Spends $85 to deliver $100 of groceries (**15% gross margin**). Tiny profit buffer.

A grocery store at $3\times$ sales would be insanely expensive, while a high-margin software company at $3\times$ sales might be a bargain.

---

## 3. Price-to-Book (P/B) — "What Are the Net Assets Worth?"

While P/E and P/S look at what a company *earns* over a year, **Price-to-Book (P/B)** looks at what the company *owns* on its balance sheet.

### What is "Book Value"?
If a company went out of business tomorrow, sold off everything it owned (buildings, machinery, cash, inventory), and paid off all its bank loans and debts, whatever is left belongs to the shareholders. That remainder is the **Book Value** (also called **Shareholders' Equity**).

$$\text{Book Value} = \text{Total Assets} - \text{Total Liabilities (Debts)}$$

$$\text{P/B Ratio} = \frac{\text{Stock Price}}{\text{Book Value Per Share}}$$

### 🏭 Real-World Example

**Midwest Steel Mill** manufactures industrial beams:
- Total Assets (factories, land, machinery, inventory, cash): **$100 Million**
- Total Debts (bank loans, supplier bills, bonds): **$40 Million**
- **Book Value:** $\$100\text{M} - \$40\text{M} = \mathbf{\$60\text{ Million}}$
- Total Shares: 1,000,000 shares $\rightarrow$ **Book Value per share = $60**

Now let's examine two possible market price scenarios:

```
┌────────────────────────────────────────┬────────────────────────────────────────┐
│ Scenario A: Stock trades at $90        │ Scenario B: Stock trades at $30        │
├────────────────────────────────────────┼────────────────────────────────────────┤
│ P/B = $90 / $60 = 1.5x                 │ P/B = $30 / $60 = 0.5x                 │
│                                        │                                        │
│ Investors are paying a 50% premium     │ The stock is selling for 50 cents on   │
│ over the net physical asset cost.      │ the dollar compared to its net assets! │
└────────────────────────────────────────┴────────────────────────────────────────┘
```

### When P/B Works Best
- **Banks & Insurance Companies:** Their assets are primarily cash, loans, and bonds that are regularly re-evaluated at current market values.
- **Capital-Intensive Businesses:** Real estate, manufacturing, shipping, and utility companies with lots of physical assets.

### Why P/B Doesn't Work Well for Tech
Companies like Apple, Google, or Microsoft have relatively small physical footprints compared to their business values. Their most valuable assets—code, algorithms, patents, and brand reputation—are **not listed as physical assets on a standard balance sheet**. That's why tech companies frequently trade at high P/B ratios (like $10\times$ or $20\times$).

---

## 4. Other "Price-to..." Balance Sheet Ratios

Beyond standard Book Value, investors look at specific slices of the balance sheet for clues about safety, liquidity, and liquidation value:

### A. Price-to-Tangible Book Value (P/TBV)
When a company buys another firm for more than its physical assets are worth, the extra premium is recorded as an accounting entry called **Goodwill**. 

$$\text{Tangible Book Value} = \text{Book Value} - \text{Goodwill \& Intangible Assets}$$

$$\text{P/TBV} = \frac{\text{Stock Price}}{\text{Tangible Book Value per Share}}$$

- **Example:** If a bank has $50 per share in total book value, but $15 of that is old merger goodwill, its tangible book value is $35. Conservatively minded investors check P/TBV to make sure they aren't paying for "paper assets" that could vanish in a write-down.

---

### B. Price-to-Cash (P/Cash)
How much are you paying relative to the cold, hard cash in the company's bank accounts?

$$\text{Price-to-Cash} = \frac{\text{Market Capitalization}}{\text{Cash and Short-Term Investments}}$$

- **Example:** A small biotechnology company has a market cap of **$40 Million**. But looking at its balance sheet, it has **$50 Million in cash** and zero debt. 
- $\text{P/Cash} = \$40\text{M} / \$50\text{M} = \mathbf{0.8\times}$.
- In this rare situation, you are buying the stock for less than the cash in its corporate treasury!

---

### C. Price-to-Working Capital (P/NWC)
Working capital is the short-term buffer a company uses to run day-to-day operations:

$$\text{Net Working Capital} = \text{Current Assets (Cash, Inventory, Receivables)} - \text{Current Liabilities (Bills due in 1 yr)}$$

$$\text{P/NWC} = \frac{\text{Market Capitalization}}{\text{Net Working Capital}}$$

- **Example:** If a retailer has $100M in cash and inventory, and owes $40M in bills due this year, its working capital is $60M. A low P/NWC ratio shows that the company has a comfortable cushion to withstand a temporary sales slump without needing emergency loans.

---

### D. The Classic "Net-Net" (Price to NCAV)
Pioneered by Benjamin Graham (Warren Buffett's mentor), **Net Current Asset Value (NCAV)** is the ultimate worst-case liquidation calculation:

$$\text{NCAV} = \text{Current Assets} - \text{Total Liabilities (ALL debts, both short & long term)}$$

Graham assumed all factories, land, and equipment were worth **$0**. If a stock traded below its NCAV ($\text{P/NCAV} < 1.0$), he considered it a guaranteed bargain—you were getting all the physical buildings and future profits completely free.

---

## 5. Cheat Sheet: Which Ratio When?

Here is a simple summary to keep in your investing toolkit:

| Valuation Metric | Statement Source | Plain English Question | Typical Example | When to Use It |
|:---|:---|:---|:---|:---|
| **P/E** *(Price-to-Earnings)* | Income Statement *(Bottom Line)* | *"How many dollars am I paying for $1 of current profit?"* | Stock = $40, EPS = $2 $\rightarrow$ **20×** | Profitable, stable, established businesses |
| **P/S** *(Price-to-Sales)* | Income Statement *(Top Line)* | *"How many dollars am I paying for $1 of customer revenue?"* | Stock = $30, Sales/sh = $10 $\rightarrow$ **3×** | Fast-growing companies that aren't profitable yet |
| **P/B** *(Price-to-Book)* | Balance Sheet *(Net Equity)* | *"Am I paying more or less than the net accounting assets?"* | Stock = $60, Book/sh = $60 $\rightarrow$ **1.0×** | Banks, insurers, real estate, manufacturers |
| **P/TBV** *(Tangible Book)* | Balance Sheet *(Hard Assets)* | *"What am I paying for the physical assets, excluding goodwill?"* | Stock = $40, TBV/sh = $30 $\rightarrow$ **1.33×** | Bank stress-testing, conservative liquidation checks |
| **P/Cash** *(Price-to-Cash)* | Balance Sheet *(Liquid Cash)* | *"How much cash does the company hold compared to its market value?"* | Mkt Cap = $40M, Cash = $50M $\rightarrow$ **0.8×** | Distressed firms, early-stage biotech, deep value |

---

## Summary: A Simple 3-Step Checklist

When looking at any company's valuation, ask three simple questions in order:

1. **Is the company profitable?**  
   $\rightarrow$ Check **P/E**. (Under $15–20\times$ is typically reasonable for moderate growth; over $30\times$ means high growth is already priced in).
2. **If it's unprofitable or growing at hyperspeed:**  
   $\rightarrow$ Check **P/S**, but always compare it against the company's gross profit margins.
3. **What is the balance sheet safety net?**  
   $\rightarrow$ Check **P/B** or **P/Cash** to see whether you have solid physical assets and cash protecting you if business conditions turn sour.
