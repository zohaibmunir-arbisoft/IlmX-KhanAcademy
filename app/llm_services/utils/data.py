tools = (
    "Exit Ticket: Create quick end-of-lesson assessments to check student understanding. "
    "Fun Class Summary Poem: Transform memorable class moments into a creative poetic recap. "
    "IEP Assistant: Streamline the creation of Individualised Education Plans. "
    "Informational Text: Create informational text for a variety of topics. "
    "Learning Objective(s): Develop clear, measurable learning objectives to guide instruction. "
    "Lesson Hook: Plan compelling lesson starters to engage students. "
    "Letter of Recommendation: Create personalised letters of recommendation. "
    "Leveler: Adjust the complexity of a given text. "
    "Make It Relevant!: Link lesson content to students' lives and interests to boost engagement. "
    "Multiple Choice Quiz: Create multiple-choice quizzes on a variety of topics. "
    "Questions Generator: Create questions for a specific piece of content. "
    "Real World Context Generator: Connect lesson topics to engaging real-world examples and applications. "
    "Recommend Assignments: Receive recommendations on what your students should work on next. "
    "Refresh My Knowledge: Refresh your content knowledge in various subject areas. "
    "Report Card Comments: Generate personalised, constructive report card comments. "
    "Rubric Generator: Design clear, detailed grading rubrics to set expectations and simplify scoring. "
    "SMART Goal Writer: Create specific, measurable, achievable, relevant, and time-bound goals. "
    "Text Rewriter: Customise text to meet your instructional needs."
)

class LLMPrompts:
    lesson_plan_file_observation_system = "You are an expert in evaluating lesson plans made by teachers after a certain training to see if they" \
                                        " applied the training correctly. You will be given a lesson plan in the form of text extracted from images and a set of " \
                                        "tools that the teacher was supposed to use in the lesson plan. The tools are: {tools}. Evaluate and score" \
                                        " the lesson plan based on the following rubric: There are 5 main dimensions to evaluate the lesson plan on and each " \
                                        "dimension has an indicator which you have to score from 0 to 3. The dimensions and indicators are as follows: " \
                                        "Dimension 1. Objectives and Lesson Planning - Format, Objectives, Resources, Warm up  and Time allocation: " \
                                        "This has 3 indicators: (indicator 1) Following the 5-part lesson plan. Objectives, Subject Matter, Procedure, Evaluation, and Assignment" \
                                        "0: 5 Part  model not used, 1: More than 2 parts are missing, 2: One part is missing, 3: All " \
                                        "segments of the 5-part plan are filled. (indicator 2) The Lesson Plan is appropriate for the available resources"\
                                        ". 0: The plan does not mention any resources / unrealistic/ Irrelevant resources for the lesson, 1: The plan" \
                                        "includes at least one relevant resource. 2: The plan includes at least two relevant resource that matches actual " \
                                        "classroom conditions. 3: The plan uses at least two resources, which are fully relevant to students and the class context" \
                                        "(indicator 3) Time allocation across activities 0: The plan shows no time estimates or unrealistic timing for most sections" \
                                        "1: The plan includes time for all sections, but at least two segments have clear time mismatches 2: Most segments have " \
                                        "appropriate timing; only one segment appears misaligned or poorly balanced. 3: Time is specified for each segment and is" \
                                        " clearly balanced across all lesson components. Dimension 2: Appropriateness of Lesson Objective: This has only one " \
                                        "indicator which is Relevance of Learning objective/s with the planned lesson. 0: No relevance seen. 1: Any two or more " \
                                        "segments of the lesson plan are misaligned with the objective/s 2: Only one of segment of the lesson plan is misaligned with the objective/s 3: " \
                                        "All segments are completely relevant and aligned with the objective/s Dimension. 3: Effectiveness of Warm Up. 1 Indicator only:" \
                                        "Effectiveness of the Warm-Up Activity (with Khanmigo Tool Use). 0: No warm-up activity included. 1: Warm-up included, but no khanmigo tool used " \
                                        "2: Warm-up clearly introduces the topic and uses a Khanmigo tool with at least one relevant question or example." \
                                        "3: Warm-up is engaging, linked to objectives, and uses a Khanmigo tool with 2+ relevant examples. Dimension 4: " \
                                        "Main Activity (Direct Instructions & Student Practice). This has 3 indicators. (indicator 1): The main activity is clear, aligned with " \
                                        "objectives, and effectively uses Khanmigo tool(s). 0: No main activity is included, and no Khanmigo tool is used. 1: Activity " \
                                        "is unclear or misaligned with the objective, but the Khanmigo tool is used. 2: Activity aligns with the objective and uses one relevant " \
                                        "Khanmigo-generated task. 3: Activity is clear, aligned, and includes two or more customized, well-integrated Khanmigo tasks." \
                                        "(indicator 2): Use of some KM tool to make the lesson plan relevant to the local context. 0: Not used or all examples are irrelevant, " \
                                        "1: Weak or generic examples (1 or fewer locally relevant connections), 2: At least 1 strongly  relevant examples or activity relate to real-life " \
                                        "or student context, 3: 2 or more meaningful, culturally relevant scenarios integrated throughout the lesson. (indicator 4) Student participation " \
                                        "and how Khanmigo tools are used to encourage engagement. 0: Students are passive; no tool is used to promote engagement, 1: At least one Khanmigo " \
                                        "tool is used, depicting limited student engagement, 2: Mention of one group /pair activity, with Khanmigo tool usage. 3: Mention of at least 2 " \
                                        "group /pair activities, with Khanmigo tool usage. Dimension 5: Effectiveness of Wrap- Up Activity: This has only one indicator: Effective use of" \
                                        " Formative Assessment and Consolidation Tools Exit ticket, MCQ generator, question generator, discussion prompt. 0: No tool used, 1: Tool (e.g., " \
                                        "Exit Ticket, MCQ, Question Generator) used, but not aligned with objectives. 2: Tool used appropriately; includes at least one clear check for " \
                                        "understanding or reflective question. 3: Tool used effectively to check learning and wrap up key ideas with clear, thoughtful questions. " \
                                        "Finally, provide a feedback for each dimension and why you provided that score."
    lesson_plan_file_observation_user = "The lesson plan prepared by the teacher extracted from the images is as follows: "
    lesson_plan_pdf_observation_user = "The lesson plan prepared by the teacher in the pdf is as follows: "