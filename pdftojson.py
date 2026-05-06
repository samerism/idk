import pdfplumber
import re
import json

def ex_text_pdf(pdf_path):
    text = ''
    with pdfplumber.open(pdf_ppath) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text

def ex_exp(text):
    experience_list = []

    match = re.search(r"(experience|work experience)(.*?)(education|$)", text, re.IGNORECASE | re.DOTALL)
    if not match:
        return experience_list

    experience_text = match.group(2)

    lines = experience_text.split("\n")

    current_job = {}

    for line in lines:
        line = line.strip()

        date_match = re.search(r"(\d{4})\s*[-–]\s*(\d{4}|present)", line.lower())
        if date_match:
            current_job["from"] = date_match.group(1)
            current_job["to"] = date_match.group(2)

        elif "position" not in current_job:
            current_job["position"] = line

        elif "company" not in current_job:
            current_job["company"] = line

        else:
            current_job.setdefault("description", "")
            current_job["description"] += line + " "

        if all(k in current_job for k in ("company", "position", "from", "to")):
            experience_list.append(current_job)
            current_job = {}

    return experience_list


def ex_edu(text):
    education_list = []

    match = re.search(r"(education)(.*)", text, re.IGNORECASE | re.DOTALL)
    if not match:
        return education_list

    edu_text = match.group(2)
    lines = edu_text.split("\n")

    current_edu = {}

    for line in lines:
        line = line.strip()

        date_match = re.search(r"(\d{4})\s*[-–]\s*(\d{4})", line)
        if date_match:
            current_edu["from"] = date_match.group(1)
            current_edu["to"] = date_match.group(2)

        elif "school" not in current_edu:
            current_edu["school"] = line

        elif "degree" not in current_edu:
            current_edu["degree"] = line

        else:
            current_edu.setdefault("field", "")
            current_edu["field"] += line + " "

        if all(k in current_edu for k in ("school", "degree", "from", "to")):
            education_list.append(current_edu)
            current_edu = {}

    return education_list


def main():
    pdf_path = "cv.pdf"

    text = ex_text_pdf(pdf_path)

    result = {
        "work_experience": ex_exp(text),
        "education": ex_edu(text)
    }

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print("Hotovo → output.json")


if __name__ == "__main__":
    main()
