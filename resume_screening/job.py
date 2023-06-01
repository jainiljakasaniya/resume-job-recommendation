import os
import pandas as pd
import resparser, match
import nltk
from nltk.corpus import stopwords
import indeed_web_scraping_using_bs4

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('universal_tagset')
nltk.download('maxent_ne_chunker')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('brown')

stopw  = set(stopwords.words('english'))

def find_sort_job(f):
    job = pd.read_csv(r'indeed_data.csv')
    job['test'] = job['description'].apply(lambda x: ' '.join([word for word in str(x).split() if word not in (stopw)]))
    df = job.drop_duplicates(subset='test').reset_index(drop=True)
    df['clean'] = df['test'].apply(match.preprocessing)
    jobdesc = (df['clean'].values.astype('U'))
    skills = resparser.skill(f)
    # skills = ' '.join(word for word in skills['skills'])
    skills = match.preprocessing(skills[0])
    # del skills[0]
    count_matrix = match.vectorizing(skills, jobdesc)
    matchPercentage = match.coSim(count_matrix)
    matchPercentage = pd.DataFrame(matchPercentage, columns=['Skills Match'])
    #Job Vacancy Recommendations
    result_cosine = df[['title','company','link']]
    result_cosine = result_cosine.join(matchPercentage)
    result_cosine = result_cosine[['title','company','Skills Match','link']]
    result_cosine.columns = ['Job Title','Company','Skills Match','Link']
    result_cosine = result_cosine.sort_values('Skills Match', ascending=False).reset_index(drop=True).head(20)
    return result_cosine


def find_sort_resume(f,link):
    os.chdir(f)
    dic = {}
    for file in os.listdir():
        lsr = []
        file_path = f"{f}\\{file}"
        if file.endswith(".pdf"):
            text = resparser.convert_pdf_to_txt(file_path)
        elif file.endswith(".doc") or file.endswith(".docx"):
            text = resparser.convert_docx_to_txt(file_path)
        lsr.append(" ".join(text))
        dic[file_path] = lsr
    fy = pd.DataFrame.from_dict(dic, orient='index')
    fy.reset_index(inplace = True)
    fy.rename(columns = {'index':'link'}, inplace = True)
    fy.rename(columns = {'0':'description'}, inplace = True)
    fun = lambda x: ' '.join([word for word in x.split() if len(word)>1 and word.lower() not in (stopw)])
    fy['description'] = fy.iloc[:,1].apply(fun)
    fy['description'] = fy['description'].apply(match.preprocessing)
    fy['Resume Title'] = fy['link'].apply(lambda x: x[x.rfind("\\")+1:len(x)+1])
    results = []
    results.append(indeed_web_scraping_using_bs4.parse_job(link))
    clean_job = fun(results[0]['description'])
    clean_job = match.preprocessing(clean_job)
    test_fy = (fy['description'].values.astype('U'))
    count_matrix = match.vectorizing(clean_job, test_fy)
    matchPercentage = match.coSim(count_matrix)
    matchPercentage = pd.DataFrame(matchPercentage, columns=['Skills Match'])
    result_cosine = fy[['Resume Title','link']]
    result_cosine = result_cosine.join(matchPercentage)
    result_cosine = result_cosine.sort_values('Skills Match', ascending=False).reset_index(drop=True).head(20)
    result_cosine = result_cosine[['Resume Title', 'Skills Match', 'link']]
    return result_cosine

    
abc = find_sort_job(r'instance\resume_files\CV2.pdf')
print(abc)