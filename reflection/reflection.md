# Application:  

# Final Reflection

This project compared three different software requirements engineering pipelines: manual, automated, and hybrid.

The **manual pipeline** produced the clearest and most human-grounded personas. Because review grouping and persona creation were performed through direct interpretation of the dataset, the resulting personas were highly realistic and emotionally aligned with user needs. The manual pipeline also produced strong requirement clarity and meaningful acceptance criteria.

The **automated pipeline** was the fastest and most reproducible. Using the Groq API with the Llama model allowed automatic grouping of reviews, persona generation, requirement generation, and test creation. However, some issues appeared in the automated outputs. In several cases, themes were overly broad, some generated personas were too generic, and a few generated requirements initially lacked sufficient specificity before refinement.

The **hybrid pipeline** produced the strongest overall results. It combined the scalability of automation with manual refinement to improve theme accuracy, persona realism, and requirement usefulness. This pipeline achieved the best balance between traceability, clarity, and efficiency.

In terms of traceability, all three pipelines achieved strong traceability links between review groups, personas, requirements, and tests. However, the hybrid pipeline provided the strongest traceability because automated outputs were manually validated and corrected.

The most useful requirements came from the hybrid pipeline because they remained grounded in real user evidence while still benefiting from automated generation speed.

Overall, this project demonstrated that while automation improves speed and reproducibility, human review remains essential for improving requirement quality, persona realism, and requirement traceability.
