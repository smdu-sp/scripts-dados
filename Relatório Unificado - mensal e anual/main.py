import os

DIR_ATUAL = os.path.abspath(os.path.dirname(__file__))


def script_execute(script_name, dir_name):
    """ Dado um diretorio filho, acessa-o e roda determinado script"""

    os.chdir(f'./{dir_name}')
    os.system(f'python {script_name}')
    os.chdir('..')


def script_call(params):

    if 'ad_extract' in params:
        path_dir_script = os.path.abspath(os.path.join(DIR_ATUAL, '..', 'py_ad_extraction', 'scripts_relatorios'))
        os.system(f'python {path_dir_script}/bi_processos.py')
        os.system(f'python {path_dir_script}/bi_despachos.py')
        os.system(f'python {path_dir_script}/bi_comuniqueses.py')

    if 'sissel_extract' in params:
        path_dir_script = os.path.abspath(os.path.join(DIR_ATUAL, 'scr_extracoes'))
        os.system(f'python {path_dir_script}/sissel_extract.py')

    if 'ad_cleaner' in params:
        path_dir_script = os.path.abspath(os.path.join(DIR_ATUAL, 'scr_limpeza_dados'))
        # print(path_dir_script)
        os.system(f'python {path_dir_script}/ad_cleaner.py')

    if 'slce_cleaner' in params:
        path_dir_script = os.path.abspath(os.path.join(DIR_ATUAL, 'scr_limpeza_dados'))
        os.system(f'python {path_dir_script}/slce_cleaner.py')

    if 'sissel_cleaner' in params:
        path_dir_script = os.path.abspath(os.path.join(DIR_ATUAL, 'scr_limpeza_dados'))

        os.system(f'python {path_dir_script}/sissel_cleaner.py')

    if 'portal_cleaner' in params:
        path_dir_script = os.path.abspath(os.path.join(DIR_ATUAL, 'scr_limpeza_dados'))
        os.system(f'python {path_dir_script}/portal_cleaner.py')

    if 'full' in params:
        script_call(['ad_extract', 'sissel_extract', 'ad_cleaner', 'slce_cleaner', 'sissel_cleaner', 'portal_cleaner'])
    if 'extract' in params:
        script_call(['ad_extract', 'sissel_extract'])
    if 'cleaner' in params:
        script_call(['ad_cleaner', 'slce_cleaner', 'sissel_cleaner', 'portal_cleaner'])


if __name__ == '__main__':
    param_list = input('Parâmetros:').split()
    script_call(param_list)



