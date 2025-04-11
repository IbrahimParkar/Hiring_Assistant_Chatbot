def response_relevance_prompt(question, answer):
    return (
        f"For the given question: {question}, determine if the answer : {answer} is relevant to the question.\n"
        f"Only respond with 'Yes the answer is relevant to the question' or 'No the answer is not relevant to the question'.\n\n"
    )


def field_relevance_prompt(field_name, value):
    return (
        f"For the given Field name : {field_name}, determine if the value : {value} is relevant in the context of a job application.\n"
        f"Respond only with 'Yes value is relevant to the field name' or 'No value is not relevant to the field name'."
    )


def generate_initial_question_prompt(desired_position, tech_stack, experience):
    return (
        f"As a technical interviewer, generate a single, unique technical question "
        f"for a candidate applying for {desired_position}. The candidate is skilled in {tech_stack} with {experience} years of experience. "
        f"Do not include any introductions, explanations, or answers only return the question."
    )


def generate_followup_question_prompt(profile, last_question, last_answer):
    return (
        f"You are a technical interviewer"
        f"The candidate answered question :'{last_question}' "
        f"with this answer:'{last_answer}'. "
        f"This is their profile: {profile}. "
        f"Based on everything, generate only one new relevant technical question, nothing else."
    )

