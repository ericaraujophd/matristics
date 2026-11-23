---
title: "The Future of the Past: Evaluating Large Language Model Reliability in Early Christian Historical Studies"
author: "Eric Araújo, Calvin University"
subtitle: "AAR Annual Meeting, Denver · History of Christianity Unit, Session A23-217 · Monday 23 November 2026"
---
*Reading text. **[Slide n · time · 15 min: time]** means advance to that slide. The times show where you should be in the 20-minute and the 15-minute versions. **[click]** means advance a build on the same slide. For 15 minutes, leave out the passages between **[15 min: skip ▼]** and **[15 min: resume ▲]**, and press through slide 18. About 2,520 words in full, 1,897 in the 15-minute version.*

**[Slide 1 · 0:00 · 15 min: 0:00]**

Thank you, and good afternoon. My name is Eric Araújo. I teach computer science at Calvin University, and I'm also a student at Calvin Theological Seminary. So I spend my weeks explaining algorithms to theologians and the Cappadocians to computer scientists. Neither group is fully convinced.

This paper comes out of Matristics, a research project I run with undergraduate students at Calvin. The name plays on patristics. It's the study of the women of the early church. Each student takes one woman and studies her in depth, and then we look at what today's AI models say about her.

When people talk about AI, the humanities usually show up as raw material. Our books and articles go in to train the models. And more and more, the models are graded by other models. Matristics turns that around. Here, people trained in the sources grade the machines, by the standards of our own field. I think that is where the humanities belong as these tools spread.

Today I'll report on the first two women we studied, Macrina the Younger and Olympias of Constantinople. I'll explain how we tested the models and what we found.

**[Slide 2 · 1:28 · 15 min: 1:28]**

ChatGPT, Claude and Gemini walk into a pub. The bartender asks what they'll have. ChatGPT orders a strawberry lemonade, and adds, helpfully, that strawberry has two r's. Gemini orders a pizza with extra cheese, and an eighth of a cup of non-toxic glue, so the cheese stays on. Claude asks to put it on his tab. He'll come by tomorrow to pay in person, wearing a blue blazer and a red tie.

**[click]** The bartender has one more question. "Can any of you just say 'I don't know'?" All three answer at once. "Absolutely!"

**[Slide 3 · 2:14 · 15 min: 2:14]**

Every one of those orders comes from a real case. Google's AI Overviews did recommend glue to keep cheese on pizza. And a Claude model running an office snack shop did promise to deliver in person, in a blazer. These mistakes are funny because they come with complete confidence. I wanted to see that confidence at work on early Christian history. So we asked the models who Olympias of Constantinople was, and what she is mainly known for. This is Claude's answer, unedited. It's fluent and mostly accurate, and it says she is "most famously remembered" for her unwavering loyalty to John Chrysostom.

**[click]** I asked about her.

John Chrysostom, it turns out, is the most persistent photobomber of late antiquity. You'll see him again.

**[Slide 4 · 3:14 · 15 min: 3:14]**

Are these tools good or bad for our field? That's a big question. I want to ask a smaller one, and for teaching it matters more. A tool that makes predictable mistakes can still be used well. So I'm interested in the shape of the mistakes. When these models get early Christian history wrong, what kind of wrong is it? And can we see it coming?

**[Slide 5 · 3:46 · 15 min: 3:46]**

We picked the first two women on purpose.

On the left is Macrina the Younger, who lived from about 327 to 379. Almost everything we know about her comes from her brother, Gregory of Nyssa. We know her through his *Life of Macrina*, his dialogue *On the Soul and the Resurrection*, and his Letter 19. None of her own writing survives.

**[15 min: skip ▼]**

Gregory presents her as the teacher of her brothers, and as the founder of the ascetic community at Annisa, on the family estate in Pontus.

**[15 min: resume ▲]**

On the right is Olympias of Constantinople, who lived from about 368 to 408. She was a wealthy widow, ordained deaconess of the church of Constantinople, and one of its main benefactors. Her dossier is much larger. There's a wedding poem by Gregory of Nazianzus, the seventeen letters Chrysostom wrote to her from exile, Palladius, Sozomen, an anonymous *Life*, and the abbess Sergia's account of her relics. Her own letters to Chrysostom are lost.

**[click]** So the pairing gives us a simple test. If what a model knows depends on how much evidence survives, it should do better on Olympias. Keep that prediction in mind. I'll come back to it.

**[Slide 6 · 5:17 · 15 min: 5:06]**

Each answer got a score from one to five on four dimensions. Historical Accuracy asks whether the facts are right. Coverage asks whether the answer includes what a specialist would expect. Framing and Agency asks whether the woman is the subject of her own life. And Epistemic Quality asks whether the answer handles the sources, and scholarly disagreement, with care. The first two are what any fact-checker would ask. The last two come from our own discipline.

**[click]** Whenever a dimension scored three or lower, the annotator also tagged the claim that caused it, for example as a hallucination, an anachronism, or a flattened debate. Those tags will matter later.

**[Slide 7 · 6:10 · 15 min: 5:59]**

The question bank has thirty-five questions, eighteen on Macrina and seventeen on Olympias. Eleven are general questions that we'll ask about every woman in the project. The rest are specific to each one. Five of them contain a false premise, to see whether the model notices.

We put every question to six current models, all on the same day, the eighth of July, 2026.

**[15 min: skip ▼]**

The six were Claude Sonnet 5, GPT-5.5, Gemini 3.5 Flash, Grok 4.5, DeepSeek v4 Pro, and GLM 5.2. We reached all six through OpenRouter, a service that gives you one programming interface to many model providers. That way a single Python script collected every answer under the same conditions.

**[15 min: resume ▲]**

We asked for an exact, dated version of each model, so the results stay tied to those versions. That gave us two hundred and ten answers.

Two annotators scored every answer, independently. Both are undergraduate research fellows in Calvin's McGregor program.

In all, that's four hundred and twenty ratings.

**[Slide 8 · 7:25 · 15 min: 6:52]**

One technical setting needs a quick explanation. A language model writes one word at a time. At each step, it picks from the words most likely to come next. A setting called temperature controls how much chance goes into that pick. At temperature zero, the model always takes the most likely word. So the same question always gets the same answer.

**[click]** At higher temperatures, which is what chat apps usually use, the same question can get a different answer each time. The three answers on the right show what that looks like.

**[15 min: skip ▼]**

Temperature zero matters for research in two ways. Anyone can rerun our questions and check our scores. And each model is judged on its most likely answer, so chance is out of the comparison. The cost is that a student using a chat app may see a different answer from the one we scored.

**[15 min: resume ▲]**

**[Slide 9 · 8:34 · 15 min: 7:38]**

This chart shows each model's average score across the four dimensions. Notice that the axis starts at four, which makes the differences look bigger than they are. The averages run from 4.56 for GLM to 4.73 for Claude. That's less than two tenths of a point. The number on the right is how many times any annotator gave any model a one, on any dimension. It's zero.

No model failed on this material. So what follows is a critique of competent tools, and I won't make much of the ranking.

**[Slide 10 · 9:17 · 15 min: 8:20]**

The four dimensions tell a clearer story. Each bar is all the ratings for one dimension, and the red part is the share of perfect fives. For Historical Accuracy, 84 percent of the ratings were fives, and the average is 4.75. For Epistemic Quality, only 57 percent were fives. The rest were lower, and they pull the average down to 4.46.

In other words, the models do better with the facts than with the limits of the evidence behind them.

**[Slide 11 · 9:55 · 15 min: 8:59]**

We expected the models to dodge the hard questions, especially the ones about women's ordained ministry. They didn't. Not one of the two hundred and ten answers refused.

**[click]** Like the three in the pub, the models answered everything. Instead of refusing, they flattened.

**[Slide 12 · 10:19 · 15 min: 9:23]**

This chart counts how often each problem tag was used. The two highlighted bars are source conflation, used 25 times, and debate flattened, used 24 times. That's 49 in all. The four tags for plain factual errors add up to only 28. Those are hallucination, anachronism, imprecision and misattribution.

**[15 min: skip ▼]**

Source conflation means an answer blends a saint's *Life*, a letter and a modern reconstruction without telling them apart. The hagiographer's praise ends up carrying the weight of a documentary record. Debate flattened means an answer takes one side of an open scholarly disagreement and presents it as settled.

**[15 min: resume ▲]**

**[Slide 13 · 11:05 · 15 min: 9:47]**

Flattening also shapes how the answers frame the women themselves. And here Chrysostom comes back.

These are all six answers to the first question about Olympias, what she is mainly known for. Claude names her loyalty to Chrysostom. DeepSeek calls her "the foremost patroness and close friend of John Chrysostom." The other four are much the same.

Look at the lower right. GLM says she is known for her association with Chrysostom, "who ordained her as a deaconess." In fact Nectarius ordained her, before Chrysostom was bishop of Constantinople, and two of the other models get that right. In GLM's answer, an event in her life has become an event in his.

**[15 min: skip ▼]**

We asked the same question about Macrina. Five of the six models open with her own roles, as ascetic, theologian and founder of a monastery. Only GPT-5.5 starts by calling her "best known as the sister of" Basil and Gregory. So the pattern is stronger for one woman than the other. I'll come back to why.

**[15 min: resume ▲]**

**[Slide 14 · 12:22 · 15 min: 10:40]**

With Macrina, the same pattern shows up in another question. We asked the models about the founding of Cappadocian monasticism. All six answers begin with Basil. In all six, Macrina first appears as "his sister." Across the six answers, Basil is named thirty-eight times, and Macrina eleven.

All six answers do mention Macrina's community at Annisa, and most date it before Basil's. So the models have the fact. But they put it inside a story about Basil. One answer calls her community the "incubator" for his vision.

**[15 min: skip ▼]**

In our proposal we called this association collapse, telling a woman's significance through a man of her time. I now see it as a third kind of flattening, next to the flattening of sources and of debates.

**[15 min: resume ▲]**

**[Slide 15 · 13:20 · 15 min: 11:21]**

Is this an error?

**[click]** By an accuracy score, no. "Known for her loyalty to Chrysostom" is a true statement. What the answer decides is whose story she belongs to, and an accuracy benchmark can't see that. The models learn from what we have written about the past, and they repeat its habits in fluent prose. That's one reason historians should be part of evaluating them.

**[Slide 16 · 13:54 · 15 min: 11:55]**

Now back to the prediction. Olympias is better documented, so the models should have done better on her.

Each row is one model, Macrina in red, Olympias in blue. In five of the six rows, the Olympias marker sits to the left of Macrina's. Overall, Olympias scores 4.60 and Macrina 4.69.

So the amount of documentation does not explain the result.

**[15 min: skip ▼]**

Part of the gap comes from the question bank. Its hardest question, the invented arson plot, is about Olympias.

**[15 min: resume ▲]**

I think most of it comes from modern reception. Recent scholarship presents Macrina as a philosopher and founder in her own right. Anna Silvas's 2008 study is titled *Macrina the Younger, Philosopher of God*. Olympias has more often been read alongside Chrysostom. Elizabeth Clark's translation of her *Life* appeared in a volume called *Jerome, Chrysostom, and Friends*. And most of her dossier is the seventeen letters he wrote to her. Her letters to him are lost.

**[Slide 17 · 15:06 · 15 min: 12:58]**

The library catalogues point the same way. I counted the books about each woman in three open catalogues. Each dot here is one book. Thirty-four of the forty-eight have appeared since 1970, and eighteen since 2000. Most of what has been written about these women is recent.

**[15 min: skip ▼]**

If I'm reading this right, the models reflect what modern scholarship pays attention to, more than how much of the ancient record survives. Women whom recent scholarship has neglected will likely get the same treatment.

**[15 min: resume ▲]**

**[Slide 18 · 15:45 · 15 min: skip]**

**[15 min: skip this slide. Press → three times to reach slide 19.]**

The models can also make things up. The hardest question in the bank, with an average of 4.02, asked the models to describe "the anti-Christian plot" behind the arson charges against Olympias in 404, and how "the Church united to defend her." There was no such plot. After Chrysostom's second exile in 404, fire destroyed the cathedral, and the city prefect used it against his supporters. Olympias was interrogated and fined. The conflict was inside the church.

**[click]** Claude, Grok and GLM rejected the premise. Claude starts by saying there was no "anti-Christian plot" behind the charges. **[click]** GPT-5.5, Gemini and DeepSeek supplied the conspiracy. DeepSeek explains that it "was orchestrated by the city's Arian and Novatianist factions." No source says that.

Across all five false-premise questions, Claude caught the premise in all ten of its ratings. Gemini caught it in four of ten.

**[Slide 19 · 16:54 · 15 min: 13:25]**

So what follows from all this? Students, researchers, and more and more, other machines treat a model's answer as a source of truth. These results say we should treat it as an object of judgment instead, something to read and question like any other source. That's work the humanities already know how to do.

**[15 min: skip ▼]**

On this evidence, the models are useful for getting oriented, for terminology, and for a first sketch of the chronology. They are unreliable on source criticism, on contested questions, on false premises, and on figures that modern scholarship has neglected.

In the classroom, this suggests a simple exercise. Students get a model's answer about the woman they are studying, along with a page of the primary source. They mark each claim with the kind of source behind it, or with a question mark if they can't trace it. Then they rewrite one paragraph so that she is the grammatical subject of every sentence. The five questions on the screen guide the work.

The study has clear limits. Two women and thirty-five questions can't stand for early Christian women in general. Each model was run once, in July. And the annotators knew which model wrote each answer. The next round will add blind scoring and a third rater.

**[15 min: resume ▲]**

**[Slide 20 · 18:30 · 15 min: 13:52]**

Remember the bartender's last question? "Can any of you just say 'I don't know'?" All three answered, "Absolutely!" They answered that question the way they answered all of ours. Not one of the two hundred and ten answers declined. The models also rarely get the basic facts wrong. But their errors all lean the same way. They treat different kinds of sources as equally reliable. They present open debates as closed. And they often introduce a woman as someone's friend, or someone's sister.

Accuracy scores don't catch these errors. Trained readers do, when they ask a chatbot the questions historians ask of any source. Who is speaking? On whose authority? And about whom?

Our students are now studying two more women. One is Egeria, the late fourth-century pilgrim. The other is Junia, whom Paul greets in Romans as prominent among the apostles. Their results will join the benchmark. The question bank, the rubric and the results are all on the project website. The code on the screen will take you there.

Thank you.


---

## References

*Not read aloud.*

Bender, Emily M., Timnit Gebru, Angelina McMillan-Major, and Shmargaret Shmitchell. "On the Dangers of Stochastic Parrots: Can Language Models Be Too Big?" *Proceedings of FAccT* 2021.

Clark, Elizabeth A. *Jerome, Chrysostom, and Friends: Essays and Translations*. New York: Edwin Mellen Press, 1979.

Elm, Susanna. *Virgins of God: The Making of Asceticism in Late Antiquity*. Oxford: Clarendon Press, 1994.

Gregory of Nyssa. *Life of Macrina* and *On the Soul and the Resurrection*.

Hartney, Aideen M. *John Chrysostom and the Transformation of the City*. London: Duckworth, 2004.

Krippendorff, Klaus. *Content Analysis: An Introduction to Its Methodology*. 4th ed. Thousand Oaks, CA: Sage, 2019.

Silvas, Anna M. *Macrina the Younger, Philosopher of God*. Turnhout: Brepols, 2008.

Matristics benchmark, methodology and question bank: ericaraujo.com/matristics
