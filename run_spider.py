#db_id
#question
#query

import spider
from datetime import datetime
#import convert_to_scheme1 as gq ##tento kod vytváří jednoduché schéma bez typů parametrů a cizích klíči, ale modely na něm paradoxně dosahují lepších výsledků
import convert_to_scheme as gq ##plnohodnotné schéma
import eval 
import time
from tqdm import tqdm

use_new_form =True
use_new_eval=False

def getTableId(g):
    return g[1]['db_id']
def getQuestion(g):
    return g[1]['question']



previous_table = ('','')
def loadTable(table_name):
    global previous_table
    if previous_table[0] == table_name:
        return previous_table[1]
    f =open("spider/database/"+table_name+"/schema.sql",'r')
    create_table_commands = ""
    lines=f.read()
    commands = lines.split(";")

    for command in commands:
        if command.strip().startswith("CREATE TABLE"):
            create_table_commands+=(command.strip() + ";\n")

    f.close()
    previous_table=(table_name,create_table_commands)
    return create_table_commands



def appendToFile(fname,q,table_id):
    fname="results/"+fname
    f1 = open(fname+"_gold.txt",'a')
    f2 = open(fname+"_pred.txt",'a')
    f3 = open(fname+"_data.txt",'a')
    f1.write(((q[0].replace('\n',' ')) +'\t'+table_id+'\n')) 
    f2.write(((q[1].replace('\n',' ')) +'\n'))  
    f3.write(((q[2].replace('\n',' ')) +'\n'))               
    f1.close()
    f2.close()
    f3.close()




def run_model_on_questions(model_name,idfrom,idto,spiderdir):#idfrom a idto včetně
    global use_new_form
    model_name=model_name.lower()
    if model_name == 'codes-1b':
        use_new_form= False
        from model_scripts import codes_1b as c1 
    elif model_name == 't5_3b_jiexing':
        use_new_form= True
        from model_scripts import jiexing as c1
    elif  model_name == 'codes-3b':
        use_new_form= False
        from model_scripts import codes_3b as c1
    elif  model_name == 't5_large':
        use_new_form= False
        from model_scripts import t5_large as c1
    elif  model_name == 't5_small':
        use_new_form= False
        from model_scripts import t5_small as c1
    elif  model_name == 'bart_large':
        ##
        from model_scripts import bart_large as c1
    elif  model_name == 'gpt2_medium':
        use_new_form= False
        from model_scripts import gpt2_medium as c1
    elif model_name =='t5_3b_cx':
        use_new_form= True
        from model_scripts import cxmefzzi as c1
    elif model_name == "test":
        pass
    else:
        print('404 MODEL NOT FOUND')
        exit(1)

    filename=model_name +'_'+ (str(datetime.now()).replace(':','').replace(' ',''))
    bench = spider.Spider()
    gen =bench._generate_examples(spiderdir+'dev.json')
    i=0
    print("\n\n")
    print(f"Test datasetu spider na modelu {model_name} zahájen")
    qwer=""
    for g in gen:#tqdm(gen,bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]",total =(idto-idfrom)):
        if i > idto:
            break##ukončení cyklu po poslední otázce  
        if i >= idfrom:
            table_id=getTableId(g)
            if table_id in ['voter_1','world_1']:  #chybějící shéma.sql
                continue
            #input_q="TABLES:" + loadTable(table_id) + "\nQUERY:"+ getQuestion(g)
            if (use_new_form== False):
                input_q="For these TABLES:\n" + loadTable(table_id) + "\nanswer this QUERY: "+ getQuestion(g)
            else:
                input_q= gq.generate_querry(getQuestion(g),table_id)
            #print(input_q)
            #result=c1.answer_my_question(input_q)                       #výsledek modelu
            
            if qwer != table_id:
                print(input_q)
                print()
            qwer=table_id

            result="SELECT count(name) FROM singer"
            time.sleep(0.01)
            
            appendToFile(filename,(g[1]['query'],result,getQuestion(g)),getTableId(g)) #zapsání do souboru kvůli evaluaci
        i+=1
        

    return filename

def eval_spider(filename):

    eval.myeval(filename)

def new_eval(filename,modelname):
    import new_eval as neweval
    neweval.eval_on_file(filename,modelname)

def run_full_spider(modelname,idfrom,idto,spiderdir):
    import time
    start=time.time()
    f=run_model_on_questions(modelname,idfrom,idto,spiderdir)
    if use_new_eval==True:    
        new_eval(f,modelname) #exec eval for custom questions
    if use_new_eval ==False:
        eval_spider(f) #evaluace
    print("\nMODEL: "+modelname+" <"+str(idfrom)+","+ str(idto)+"> " +"TIME: "+str(time.time() -start))



import sys

def main():
    spiderdir="spider/"
    if len(sys.argv) == 5:
        spiderdir=sys.argv[4]+"spider/"

    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print("Usage: python run_spider.py [modelname] [fromid] [toid]")
        print("Available model names: \ncodes-1b, \ncodes-3b, \nt5_small, \nt5_large, \nbart_large, \ngpt2_medium, \nt5_3b_jiexing, \nt5_3b_cx")
        print("Test question: from 0 to 1000 (0 and 1000 included)")
        print("Exemple: python run_spider.py t5_small 0 1000    ##runs question from 0(included) to 1000(included) on model t5_small")
        return

    modelname = sys.argv[1]
    fromid = sys.argv[2]
    toid = sys.argv[3]

    run_full_spider(modelname, int(fromid), int(toid),spiderdir)
    print("DONE")

if __name__ == "__main__":
    main()
