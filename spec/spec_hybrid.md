# Requirement ID: HFR1
- Description: The system shall provide empathetic emotional support responses to users experiencing distress, anxiety, or negative thoughts within 2 seconds.
- Source Persona: Emotionally Vulnerable Support Seeker
- Traceability: Derived from hybrid group H1
- Acceptance Criteria: Given a user enters a message expressing anxiety, sadness, or emotional distress, when the chatbot receives the message, then it must return an empathetic and supportive response within 2 seconds.

# Requirement ID: HFR2
- Description: The system shall avoid responses that intensify a distressed user’s emotional state.
- Source Persona: Emotionally Vulnerable Support Seeker
- Traceability: Derived from hybrid group H1
- Acceptance Criteria: Given a user expresses hopelessness or emotional distress, when the chatbot generates a response, then the response must not include dismissive, blaming, or emotionally harmful language.

# Requirement ID: HFR3
- Description: The system shall provide guided CBT exercises that help users identify and reframe negative thought patterns.
- Source Persona: Self-Guided Wellness Improver
- Traceability: Derived from hybrid group H2
- Acceptance Criteria: Given a user opens the CBT tools section, when the user selects a CBT activity, then at least one guided exercise with actionable steps must be displayed.

# Requirement ID: HFR4
- Description: The system shall provide guided mindfulness, breathing, and meditation exercises through the wellness tools interface.
- Source Persona: Self-Guided Wellness Improver
- Traceability: Derived from hybrid group H2
- Acceptance Criteria: Given a user accesses wellness tools, when a breathing or meditation exercise is selected, then the exercise must start successfully and remain usable until completion.

# Requirement ID: HFR5
- Description: The system shall maintain relevant conversation memory across sessions for returning users.
- Source Persona: Personalized Conversation User
- Traceability: Derived from hybrid group H3
- Acceptance Criteria: Given a returning user resumes a previous conversation, when the user sends a follow-up message, then the chatbot must reference relevant prior context from the same conversation history.

# Requirement ID: HFR6
- Description: The system shall generate contextually relevant responses that reduce repetitive, scripted, or generic replies.
- Source Persona: Personalized Conversation User
- Traceability: Derived from hybrid group H3
- Acceptance Criteria: Given a user submits two different prompts with different emotional contexts, when the chatbot responds, then each response must be specific to the prompt and must not repeat the same generic wording.

# Requirement ID: HFR7
- Description: The system shall support multilingual interaction for supported non-English languages.
- Source Persona: Inclusive Access User
- Traceability: Derived from hybrid group H4
- Acceptance Criteria: Given a user selects a supported non-English language, when the user navigates the app and sends a message, then interface labels and chatbot responses must appear in the selected language.

# Requirement ID: HFR8
- Description: The system shall support accessible navigation for users relying on assistive technologies such as screen readers.
- Source Persona: Inclusive Access User
- Traceability: Derived from hybrid group H4
- Acceptance Criteria: Given a user enables assistive technology, when the user navigates key application features, then the main interface, chat area, and wellness tools must remain accessible.

# Requirement ID: HFR9
- Description: The system shall clearly display subscription pricing, plan options, and premium feature differences before purchase.
- Source Persona: Cost-Conscious Premium Evaluator
- Traceability: Derived from hybrid group H5
- Acceptance Criteria: Given a user opens the premium subscription page, when subscription options are shown, then each plan must clearly display its price, billing period, and included premium features.

# Requirement ID: HFR10
- Description: The system shall clearly display free trial, billing start date, and cancellation information before premium activation.
- Source Persona: Cost-Conscious Premium Evaluator
- Traceability: Derived from hybrid group H5
- Acceptance Criteria: Given a user starts a free trial or premium sign-up flow, when the billing details page is displayed, then the billing start date, trial duration, and cancellation information must be clearly visible before confirmation.