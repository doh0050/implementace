def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        result= file.read()
    return result

#dbtext='WITH THIS DATABASE SCHEME:\n'
dbtext='S TÍMTO SCHÉMA DATABÁZE:\n'
#qtext='\nWRITE SQL QUERY FOR THIS QUESTION:\n'
qtext='\nNAPIŠ SQL DOTAZY PRO TYTO OTÁZKY:\n'

###MODELY
#
#import cxmefzzi as j
#import codes_3b as j
#import codes_1b as j
#import gpt2_medium as j
#import t5_large as j
#import t5_small as j
#import bert_large as j

##schéma tabulek
#
scheme_file_path='ds1_db.sql'
#scheme_file_path='ds1_db_sheme.sql'
#scheme_file_path='ds1_db_eng.sql'
#scheme_file_path='ds1_db:scheme_eng.sql'

##otázky
#
#questions_file_path='ds1_easy.txt' #jednoduché dotazy pro otestování zda model zvládá ČJ
questions_file_path='ds1_otazky.txt'
#questions_file_path='ds1_otazky_eng.txt'

i=0
otazky=load_file(questions_file_path).split("\n")
dbscheme=load_file(scheme_file_path)
for o in otazky:
    finalquery=dbtext+dbscheme+qtext+o

    print(f"{finalquery}\n")
    #print(f'ID {i} Q: {o}')
    #print(j.answer_my_question(finalquery))
    #print("")


