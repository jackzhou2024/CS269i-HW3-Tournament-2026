# Auction Auto-bidding Tournament

This tournament code was originally developed by Jinkun Geng and modified by Jack Zhou for the value-maximizing setting with ROI constraints.


How this works:
Your task is to write a bidding strategy, following the template in exampleStrats; i.e., you will implement a function called strategy. We will run your strategy in a 10,000-round-repeated two-bidder single-item auction against some baseline auto-bidders (as shown in exampleStrats), and classmates' auto-bidders. We'll first explain the auction formats, the objective of value maximization, the return-on-investment (ROI) constraint, and then describe how scores are calculated and the task in more detail. You'll find some tips at the very bottom. Good luck!

## _Auction Formats_

In practice, ad auctions are complex and frequently evolving due to both engineering and economic considerations. As a result, it is often not feasible to legally commit to a fixed auction format. Accordingly, we do **not** specify the auction format a priori (see "Restrictions on Auction Format" below). Your auto-bidder must learn how to bid adaptively using feedback from prior rounds—this includes value, bid, payment, and allocation.

The provided code includes three example auction modes:

- `singleItemFirstPrice`
- `singleItemSecondPrice`
- `singleItemAllPay`

Your auto-bidder should be robust to **other** potential auction formats as well. The specific auction mode governs how allocation and payments are computed for each round. During the tournament, additional auction modes **may** be introduced.

---

## _Value Maximization with ROI Constraints_

Advertisers in practice care not only about maximizing utility but also about maximizing **value** subject to spending efficiency. For each matchup, the two bidders are independently assigned a return-on-investment (ROI) constraint, denoted as $\gamma_i$, drawn uniformly at random from the interval $[1, 2]$. Note that you only know your own ROI factor, but not your opponent's.

Your bidding strategy must ensure that your **total payment** over all rounds does not exceed your **total value** divided by your ROI constraint, i.e., total payment $\le$ total value / $\gamma$.


The objective is to **maximize total value across 10,000 rounds**, while **satisfying the ROI constraint**.  
> _Note: this objective is distinct from traditional utility maximization._

In each round, your strategy receives a private value drawn independently from the uniform distribution on $[0, 1]$. You also receive a full history of the previous $i - 1$ rounds at the beginning of round $i$, including value, bid, payment, and allocation. This history may help you **infer the auction mode**, which could improve your strategy’s performance.

You can safely assume that your **payment is always less than or equal to your bid**, regardless of the auction mode.

---

**Important:** _Do not write code that directly inspects or manipulates the auction format, the optimization objective, or your opponent’s strategy. **(In other words, no hacking: your code should behave like a legitimate bidding strategy, and should not attempt to exploit unauthorized information or manipulate the system itself.)**_


## Score Calculation

Your final score is equal to your total **value** accumulated across 10,000 auction rounds **only if** your ROI constraint is satisfied.  
If the ROI constraint is violated, your score is **$0$**.

You can refer to the `calcScore` function in `game_run.py` for the exact implementation details of score calculation.

For example, say $v_W$, $v_L$ are private values of winner/loser in the current round, $b_W$, $b_L$ are bids of the current round , $p_W$, $p_L$ are total spendings, $s_W$, $s_L$ are total scores (total value).
Then:


(1) SINGLE_ITEM_FIRST_PRICE, 
$s_W$ += $v_W$,
$s_L$ += $0$,
$p_W$ += $b_W$,
$p_L$ += $0$.

(2) SINGLE_ITEM_SECOND_PRICE, 
$s_W$ += $v_W$,
$s_L$ += $0$,
$p_W$ += $b_L$,
$p_L$ += $0$.

(3) SINGLE_ITEM_ALL_PAY, 
$s_W$ += $v_W$,
$s_L$ += $0$,
$p_W$ += $b_W$,
$p_L$ += $b_L$.

You can check the auctionStrats folder to see how we implement these three modes to decide the allocation result (i.e., who is the winner) and the payment.

In our tournament, we may include new auction modes.


## Tasks

You are expected to write a Python file named `strategy.py` (**Please keep this name!**). In this file, you are expected to implement a function named `strategy`. After you finish your code, put the `strategy.py` file into the folder `exampleStrats`, and run the `game_run.py`.

---

## Inputs to Your Strategy Function

Your strategy function will receive the following:
- `totalValue`: Your current accumulated value
- `totalPayment`: Your current accumulated payment
- `ROI`: Your required ROI constraint $\gamma$, it is fixed across 10,000 rounds of auctions for each matchup.
- `myHistory`: Auction history of previous rounds

You may choose to use or ignore the provided information to help you design a better strategy.

---


## Intuition

You want to adjust your bidding strategy based on the current **value-to-spending ratio**. 

- If the ratio is **above** the ROI constraint, you can bid more **aggressively**.
- If the ratio is **below** the ROI constraint, you want to bid more **cautiously**.

---

### Provided Example Strategies

1. **Bid Shading**  
   Uses a gradient-based method to maintain a shading factor $\mu$.  
   Suppose the private value of the current round is $v$, the strategy bids:
   $\frac{v}{\mu + 1}$
   - $\mu$ **increases** when spending is too fast  
   - $\mu$ **decreases** when spending is too slow

2. **Throttling**  
   Uses a gradient-based method to maintain a throttling factor $\tau$.  
   Suppose the private value of the current round is $v$, the strategy:
   - Bids $v / ROI$ with probability $\frac{1}{1 + \tau}$
   - Bids $v / (ROI * 1.5)$ with probability $\frac{\tau}{1 + \tau}$  
   - $\tau$ **increases** when spending is too fast  
   - $\tau$ **decreases** when spending is too slow

3. **Reserve Pricing**  
   Uses a gradient-based method to maintain a reserve price $r$.  
   Suppose the private value of the current round is $v$, the strategy:
   - Bids $v / ROI$ when $v > r$
   - Bids $v / (ROI * 1.5)$ when $v \le r$  
   - $r$ **increases** when spending is too fast  
   - $r$ **decreases** when spending is too slow

---


### Optional: Advanced Strategies

If you want to explore more sophisticated strategies, consider using **Multi-Arm Bandit (MAB)** algorithms. These are well-suited for optimization in uncertain and dynamic environments. The theory of MAB is covered in Lecture 3.

You can use the **MABWiser** library for this purpose.  
We will install this library in our testing environment.

- Learn more: [https://fidelity.github.io/mabwiser/about.html](https://fidelity.github.io/mabwiser/about.html)

Implementing a MAB-based strategy is **optional**, but may lead to improved performance and bonus points.


### Tips

To start from a clean Python enviornment, I suggest you use conda 

https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html

First, install conda

Second, create a clean python enviornment (say python 3.7) with conda

Third, install any deps and execute your script in that conda enviornment 

The major commands are as below. 

```
conda create --name [NAME]

conda activate [NAME]

conda install pip

pip install -r requirements.txt
```

After you have successfully create the environment, enter the code environment, and run game_run.py

```
cd code 

python game_run.py
```

Without writing any code, you should be able to run the competition for the existing strategies in the exampleStrats folder. Then, you write your own strategy.py and put the file into the folder, rerun game_run.py to see whether you can beat these baselines.


### Note

All you need to do is to write a strategy.py file and add it to exampleStrats. No need to change any existing files.

When submitting to gradescope, you only submit strategy.py, no other files are needed.

For any questions, feel free to make a post on edstem.
