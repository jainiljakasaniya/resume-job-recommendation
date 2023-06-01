import os
from flask import Flask,render_template,redirect,request
from resume_screening import job
from os import listdir

# import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('universal_tagset')
# nltk.download('maxent_ne_chunker')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('brown')

from nltk.corpus import stopwords

stopw  = set(stopwords.words('english'))

# jobs = pd.read_csv(r'indeed_data.csv')
# jobs['test'] = jobs['description'].apply(lambda x: ' '.join([word for word in str(x).split() if word not in (stopw)]))
# df = jobs.drop_duplicates(subset='test').reset_index(drop=True)
# df['clean'] = df['test'].apply(match.preprocessing)
# jobdesc = (df['clean'].values.astype('U'))

app=Flask(__name__)

os.makedirs(os.path.join(app.instance_path, 'resume_files'), exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/employee')
def employee():
    return render_template('employee.html')

@app.route('/employeer')
def employeer():
    return render_template('employeer.html')

@app.route("/home")
def home():
    return redirect('/')


@app.route('/employee_submit',methods=['POST'])
def employee_submit_data():
    if request.method == 'POST':        
        f=request.files['userfile']
        f.save(os.path.join(app.instance_path, 'resume_files', f.filename))
        
    path = 'instance/resume_files/{}'.format(f.filename)
    result_cosine = job.find_sort_job(path)
    return render_template('employee.html', column_names=result_cosine.columns.values, row_data=list(result_cosine.values.tolist()),
                           link_column="Link", zip=zip)

@app.route('/employeer_submit',methods=['POST'])
def employeer_submit_data():
    my_path = r"instance\resume_files"
    for file_name in listdir(my_path):
        file_path = f"{my_path}\\{file_name}"
        os.remove(file_path)
    if request.method == 'POST':        
        f = request.files.getlist("userfile")
        for file in f:
            file.save(os.path.join(app.instance_path, 'resume_files', file.filename))
        result_cosine = job.find_sort_resume(f = r"instance\resume_files",link = 'https://in.indeed.com/viewjob?jk=56c808776a6c49db&tk=1gbhet5m92ek1000&from=serp&vjs=3')
        return render_template('employeer.html', column_names=result_cosine.columns.values, row_data=list(result_cosine.values.tolist()),
                               link_column="link", zip=zip)
        # print(f)
        # return ""
            
    
    # skills = resparser.skill('instance/resume_files/{}'.format(f.filename))
    # skills.append(match.preprocessing(skills[0]))
    # del skills[0]

    # count_matrix = match.vectorizing(skills[0], jobdesc)
    # matchPercentage = match.coSim(count_matrix)
    # matchPercentage = pd.DataFrame(matchPercentage, columns=['Skills Match'])

    # #Job Vacancy Recommendations
    # result_cosine = df[['title','company','link']]
    # result_cosine = result_cosine.join(matchPercentage)
    # result_cosine = result_cosine[['title','company','Skills Match','link']]
    # result_cosine.columns = ['Job Title','Company','Skills Match','Link']
    # result_cosine = result_cosine.sort_values('Skills Match', ascending=False).reset_index(drop=True).head(20)

    # return render_template('employee.html', column_names=result_cosine.columns.values, row_data=list(result_cosine.values.tolist()),
    #                        link_column="Link", zip=zip)

if __name__ =="__main__":
    app.run()