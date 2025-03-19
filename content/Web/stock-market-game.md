Title: The Stock Market Game, made easy with Phoenix LiveView
Date: 2025-03-03
Status: published
Tags: phoenix, elixir

A couple years ago my wife, who is an 8th grade US History teacher, came to me for help with a spreadsheet to simulate the US stock market leading up to the crash in 1929. The spreadsheet was cumbersome, very complicated for the students, and a major pain for her to grade. The point of the lesson is to lead the students to buying stocks on huge margins to recreate the conditions that led to the collapse, but the math for calculating loans and debt was too complicated. And this wasn't a math class.

So I did the completely normal thing, and decided to implement it as a web app using [Phoenix LiveView](https://phoenixframework.org/). The advantages were many, for the students and for my wife. What used to be a major time sink for her that took up huge portions of her class time, and was too complicated to be fun for the kids, turned into a 5 minute/day activity that the kids absolutely loved. The whole school is abuzz with talk of, "What's your equity dude" and "I think I'm over leveraged." With this being the third year of the lesson, kids have actually been asking all year when they were going to play the stock market game they had heard about for years.

![The Student Worksheet]({static}/images/stock-market-game/worksheet_scrambled_day3.png "The Student Worksheet, Day 5")

The advantages of doing this proved to be overwhelmingly worth the time it took for me to code it all up. The lesson now just takes 5 minutes a day in each class, during which the students can make their daily buys and sells (though many are refreshing away before class to catch the new prices, with cries of joy and pain heard through the school), and also so they can see a big leaderboard on the projector for their class and the whole school.

![Leaderboard Day 5]({static}/images/stock-market-game/leaderboard_day5.png "Leaderboard, Day 5")

With LiveView, they get instant feedback as they work on their worksheet for the day, with many helpful errors, and min/max hints so they know what they can do for each decision. And since all the logic and form validation is done server-side, there is no chance for them to cheat, and I didn't have to implement the same complicated form validation on both front-end and back-end.

The goal of the multi-day lesson is to push them to over-borrow, so that when the market inevitably collapses, they have a first-hand experience of what it was like to get drunk on huge numbers. They all start with merely $1000 each, but they can borrow up to 90% of a stock purchase. (Believe it or not, this was common in the early 20th century!) It is not uncommon to see numbers in the billions and trillions.

We purposely created the leaderboard (something not possible with spreadsheets before!) to foster competition. To get the biggest numbers, you should sell everything every day, if it went up in price, pay back the minimum 10% to the broker, then buy even more at 90% margin. But the kids never know how many days the game is going to go on, so it's all about pushing your luck. The riskiest players stand to make the most money, but also to lose the most.

Also, since this is the third year, previous students get involved a lot. In one example, this year a previous student was seen parading up and down the 8th grade hallway talking about how much they made last year when they won the game. She even had to vary up the stocks this year, because certain stocks have become legend for making billionaires.

So today brought the year's lesson to a close, and I thought I'd write up this quick retrospective. Today she "crashed" the market, but reducing all share prices by less than 100%. Every stock ends up higher than what it started as, but due to the successful psychological cues, the ease of borrowing money, and the push to be at the top of the leaderboards, so far every year the market has truly crashed.

Inevitably, the winners with a positive balance at the end will ask, "When am I getting paid?"

![Leaderboard Last Day Top]({static}/images/stock-market-game/leaderboard_last_day_top.png "Leaderboard, Last Day, Top")

To which my wife can respond, "I can pay you as soon as every else pays me what they owe!"

![Leaderboard Last Day Bottom]({static}/images/stock-market-game/leaderboard_last_day_bottom.png "Leaderboard, Last Day, Bottom")

>***Note for Students!**: If you happen to find this article, and you're a student or future student, just know that all the data in the screenshots has been scrambled or fabricated. Have a good game!*
