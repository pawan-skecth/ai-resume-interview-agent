from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')


def embedding_skill_matching(detected_skills, required_skills):

    matched_skills = []
    missing_skills = []

    # convert to embeddings
    req_embeddings = model.encode(required_skills)
    det_embeddings = model.encode(detected_skills)

    for i, req in enumerate(required_skills):

        req_vec = req_embeddings[i].reshape(1, -1)

        similarities = cosine_similarity(req_vec, det_embeddings)[0]

        max_score = np.max(similarities)

        if max_score >= 0.55:   # semantic threshold

            matched_skills.append(req)

        else:

            missing_skills.append(req)

    score = int((len(matched_skills) / len(required_skills)) * 100)

    return score, matched_skills, missing_skills