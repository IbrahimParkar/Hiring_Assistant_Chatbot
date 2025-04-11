import streamlit as st
from utils import *

# Set the title for the Streamlit app
st.title("🤖 TalentScout - AI Hiring Assistant")

# Display welcome message and start button if form has not yet been shown
if "show_form" not in st.session_state:
    st.session_state.show_form = False

if not st.session_state.show_form:
    st.subheader("Welcome to TalentScout!")
    st.write("Hello! I am your AI Hiring Assistant. I help with the initial screening process by collecting your "
             "details and assessing your technical skills.")
    st.write("Click the button below to start your application process!")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Get Hired!", use_container_width=True):
            st.session_state.show_form = True
            st.rerun()

# Show candidate form only if not yet submitted
if st.session_state.show_form and "form_submitted" not in st.session_state:
    st.header("Candidate Information")

    # Collect basic user details
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    contact_number = st.text_input("Contact Number")
    location = st.text_input("Location (City, Country)")
    experience = st.number_input("Years of Experience", min_value=0, max_value=50)
    desired_position = clean_input(st.text_area("Enter your desired position(s)"))
    tech_stack = clean_input(st.text_area("Enter your tech stack (comma-separated)"))

    # Show privacy notice and get consent
    st.markdown("**Consent Required**")
    with st.expander("View Privacy Notice"):
        st.markdown(
            """
            By proceeding, you agree to share your personal information (name, email, phone number, etc.) for recruitment purposes only.  
            All data collected will be handled securely and will not be used for any purpose other than evaluating your fit for a technical position at TalentScout.

            You may request to have your data deleted at any time by contacting us at [privacy@talentscout.ai](mailto:privacy@talentscout.ai).
            """
        )
    consent = st.checkbox("I agree to the Privacy Notice if you wish to proceed.")
    if not consent:
        st.warning("Please accept the Privacy Notice to continue.")
        st.stop()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        proceed_clicked = st.button("Proceed", use_container_width=True)

    if proceed_clicked:
        # Validation checks
        if not is_valid_email(email):
            st.warning("⚠️ Please enter a valid email address.")
        elif not is_valid_contact_number(contact_number):
            st.warning("⚠️ Please enter a valid contact number (with or without country code).")
        elif not tech_stack.strip() or not desired_position.strip():
            st.warning("⚠️ Please fill in both Tech Stack and Desired Position fields.")
        elif not is_field_relevant("Tech Stack", tech_stack):
            st.warning("⚠️ Please enter a relevant Tech Stack. Example: Python, SQL, React")
        elif not is_field_relevant("Desired Position", desired_position):
            st.warning("⚠️ Please enter a relevant Desired Position. Example: Data Analyst, Backend Developer")
        else:
            # Store candidate profile data in session
            st.session_state.profile = {
                "name": name, "email": email, "contact_number": contact_number,
                "location": location, "experience": experience,
                "desired_position": desired_position, "tech_stack": tech_stack
            }
            st.session_state.form_submitted = True

            # Initialize session state variables for interview
            st.session_state.questions = []
            st.session_state.responses = {}
            st.session_state.current_question = 0
            st.session_state.history = []

            # Generate first question
            prompt = generate_initial_question_prompt(desired_position, tech_stack, experience)

            with st.spinner("Generating your first question..."):
                first_question = query({"inputs": prompt})

            if "Error" not in first_question:
                st.session_state.questions.append(first_question)
                st.session_state.current_question = 0
                st.rerun()
            else:
                st.error("⚠️ Sorry, we couldn't generate a question. Please try again!")

# Show interview questions one at a time once form is submitted
if "form_submitted" in st.session_state and not st.session_state.get("interview_complete", False):
    total_questions = 4
    current_q_idx = st.session_state.current_question

    if current_q_idx < len(st.session_state.questions):
        st.subheader(f"Question {current_q_idx + 1} of {total_questions}")
        st.write(f"**{st.session_state.questions[current_q_idx]}**")

        response_key = f"response_{current_q_idx}"
        user_response = st.text_area("Your Response", key=response_key, height=100)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if current_q_idx < total_questions - 1:
                next_button = st.button("Next Question", use_container_width=True)
            else:
                complete_button = st.button("Complete Interview", use_container_width=True)

        if current_q_idx < total_questions - 1 and next_button:
            cleaned_response = clean_response(user_response)

            if not cleaned_response.strip():
                st.warning("⚠️ Please provide a response before proceeding!")
            else:
                partial_response_for_check = get_first_n_lines(user_response, n=3)

                with st.spinner("🔍 Parsing your response..."):
                    is_relevant = is_response_relevant(
                        st.session_state.questions[current_q_idx],
                        partial_response_for_check
                    )

                if not is_relevant:
                    st.warning(
                        "⚠️ Your response does not seem to be relevant to the question. Please revise your answer before proceeding."
                    )
                else:
                    # Step 2: Store only if relevant
                    st.session_state.responses[response_key] = cleaned_response
                    summarized_answer = summarize_text(cleaned_response)

                    st.session_state.history.append({
                        "question": st.session_state.questions[current_q_idx],
                        "answer": summarized_answer
                    })

                    # Prepare prompt for the next follow-up question
                    interview_context = (
                        f"Candidate Profile:\n"
                        f"Name: {st.session_state.profile['name']}\n"
                        f"Experience: {st.session_state.profile['experience']} years\n"
                        f"Position: {st.session_state.profile['desired_position']}\n"
                        f"Tech Stack: {st.session_state.profile['tech_stack']}\n\n"
                        f"Previous Questions & Responses:\n"
                    )
                    for idx, qa in enumerate(st.session_state.history):
                        interview_context += f"Q{idx + 1}: {qa['question']}\nA{idx + 1}: {qa['answer']}\n\n"

                    followup_prompt = generate_followup_question_prompt(
                        profile=st.session_state.profile,
                        last_question=st.session_state.history[-1]['question'],
                        last_answer=st.session_state.history[-1]['answer']
                    )

                    with st.spinner("🤖 Generating your next question..."):
                        next_question = query({"inputs": followup_prompt})

                    if "Error" not in next_question:
                        st.session_state.questions.append(next_question)
                        st.session_state.current_question += 1
                        st.rerun()
                    else:
                        st.error("⚠️ Error generating next question. Please try again.")

        if current_q_idx == total_questions - 1 and complete_button:
            cleaned_response = clean_response(user_response)

            if not cleaned_response.strip():
                st.warning("⚠️ Please provide a response before completing the interview!")
            else:
                # Relevance check before storing
                is_relevant = is_response_relevant(
                    st.session_state.questions[current_q_idx],
                    cleaned_response
                )

                if not is_relevant:
                    st.warning(
                        "⚠️ Your response does not seem to answer the question. Please try again with a more relevant answer.")
                else:
                    # Store only if relevant
                    summarized_answer = summarize_text(cleaned_response)
                    st.session_state.responses[response_key] = cleaned_response

                    st.session_state.history.append({
                        "question": st.session_state.questions[current_q_idx],
                        "answer": summarized_answer
                    })

                    # Save all responses to a file
                    interview_data = {
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Name": st.session_state.profile["name"],
                        "Email": st.session_state.profile["email"],
                        "Phone": st.session_state.profile["contact_number"],
                        "Position": st.session_state.profile["desired_position"],
                        "Tech Stack": st.session_state.profile["tech_stack"],
                        "Experience": st.session_state.profile["experience"],
                        "QnA History": st.session_state.history,
                    }

                    save_interview_to_file(interview_data)

                    # Reset state and show final message
                    st.session_state.interview_complete = True
                    st.session_state.questions = []
                    st.session_state.responses = {}
                    st.session_state.current_question = 0
                    st.session_state.history = []
                    st.rerun()

# Final screen after completion
elif st.session_state.get("interview_complete", False):
    st.subheader("Interview Complete")
    st.success("Thank you for completing the interview! We'll be in touch shortly. 🎉")
