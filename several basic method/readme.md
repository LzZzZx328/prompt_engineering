prompt工程的一些思想实现，包括：<br>
1.基本的思维链CoT，Few-Shot CoT、Zero-Shot CoT;<br>
2.Reflection的Self-Refine;<br>
3.Planning and Execute;<br>
4.Tools Use;<br>
5.ReAct 


chain of thought:也就是 COT ，一经提出就引发了社区对它的热烈讨论，类似 AI 是不是也需要鼓励来获得更好的表现之类的问题<br>
这篇文章中说，只要在每个答案之前加上一句“Let's think step by step”，就可以立即在两个比较困难的数学问题数据上涨点，而且涨点非常明显<br>
由于这个方法比较简单，只是加了一句话就能够非常明显地涨点，所以立即引发了大家对于这一领域的关注，也就是“ AI 是不是也需要鼓励来获得更好的表现”<br>
<br>
这里以需要推理的数学题举例<br>
1、Zero-shot<br>
文献：Large Language Models are Zero-Shot Reasoners(https://arxiv.org/abs/2205.11916)<br>
语言模型的输入是一道数学题连接一个字符串“The answer is”，然后让语言模型进行续写<br>
<br>
2、Zero-Shot-CoT<br>
语言模型的输入还是一道数学题连接一个字符串“Let's think step by step”，然后让语言模型进行续写<br>
这种情况下，语言模型会续写出中间推理步骤，并最终生成答案<br>
<br>
3、Manual-CoT<br>
文献：Chain of Thought Prompting Elicits Reasoning in Large Language Models（https://arxiv.org/abs/2201.11903）<br>
这种情况下使用到了少样本学习，在输入问题之前，手动设计一些问题和答案的样例（样例的答案给出中间推理步骤），这些问题和答案都需要手动构造，所以叫 Manual-CoT<br>
语言模型的输入是一些手动设计的问题和答案的参考样例连接一个真正需要求解的问题，然后让语言模型进行续写<br>
这里少样本训练中的问题和答案的样例都需要人为构造并手动设计，因此为了和第四种自动 CoT 做区分，这里称为 Manual-CoT<br>
Manual-CoT 比 Zero-Shot-CoT 的性能要好，因为它采用的是 few shot ，在输入中提供了一些问题、中间推理步骤以及答案的样例给语言模型进行参考。但是，提供这些样例需要进行人工设计，这就需要一定的人工成本<br>
question-rationale-answer（demonstrations）+test question—>llm—>rationale+answer<br>
<br>
4.Self-Refine<br>
文献：Self-Refine: Iterative Refinement with Self-Feedback(https://arxiv.org/abs/2303.17651)<br>
核心思想：让大模型学会总结反思，跟 LLM 的多次交互，每次交互让 LLM 扮演不同的角色执行不同的任务从而得到最终的结果<br>
<br>
5.ReAct<br>
文献：ReAct: Synergizing Reasoning and Acting in Language Models(https://arxiv.org/abs/2210.03629)<br>
核心思想：让大模型把理由reason写进提示词里<br>
大模型的记忆是记住用户的问题，但不会记住自己在回答用户问题的搜索思考流程，问下个问题时，这个思维过程就失去了。所以把大模型的思考方式写出来，让它对自己的行为有记忆。<br>
通过大模型的常识缩小动作空间<br>
