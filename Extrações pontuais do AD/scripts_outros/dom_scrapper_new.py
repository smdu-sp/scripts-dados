import requests
import pandas as pd
import json
import time


year = 2023
meses = ['03', '04', '05', '06', '07', '08', '09', '10']

url = 'https://diariooficial.prefeitura.sp.gov.br/md_epubli_controlador.php?acao=edicao_download'

headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding":  "gzip, deflate, br",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Length": "109",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": "PHPSESSID=1gpuh8eo4i8fhdq8cb32q4btud; TS017e7eac=0181a10bc73f7a19a725197317a0168c0c98753eec7589fe92c6328a8d2a745f6601c8224e62e5ff3b9c15e011cf01d0311a980711b13af1a724f4e19275b7412e26ca0e13; TSPD_101=083a958c66ab2800730cc88d103cb05c533726070bb434941ed132619c245367c876da2d26c0df6582ebb74cd8e3b20808667978fe051800941c8080378f15a9b0670ecd9408ab774f29f86acc1fe506; _gid=GA1.4.2073481533.1690825781; _gat_gtag_UA_47129721_1=1; _ga=GA1.1.1523591394.1690825781; _ga_3QFYNDJNFG=GS1.1.1690825781.1.1.1690825801.0.0.0; TS3b4d9fc0077=083a958c66ab28006047edbfd07684a00263c8ae4939dc52db1471ea48101e2b73a3f307fe64e9921ba93b1ea125037808b25661821720000a1dcca6b0cb3f73f4f648165c208d6b595ad59f8ebb0ab86d65df2b4af74e42; TS3b4d9fc0029=083a958c66ab28008c83803fcbaca44f09661c9117aa370887105b0a1473c6e6b3fa1bc3ab839d4d0d3a2ac0bb9a601c; TS9482b27c027=083a958c66ab2000d77cc765deeaf99b860b70d06e2b9b4c8f23bf07f67f0bed28168436fa628a9e08646014021130001768ff1ea625363dc1640407223725c336b96c76702dac7ae9b8f278a516ab41fd101eb6c42c46db8ce18a92fb2a1219",
            "Host": "diariooficial.prefeitura.sp.gov.br",
            "Origin": "https://diariooficial.prefeitura.sp.gov.br",
            "Referer": "https://diariooficial.prefeitura.sp.gov.br/md_epubli_controlador.php?acao=edicao_consultar&formato=A",
            "Sec-Ch-Ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            "Sec-Ch-Ua-Mobile": r"?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            }


for i in meses:
    data_container = []

    for k in range(1, 32):
        data_edicao = f'{str(k).zfill(2)}/{i}/{year}'

        payload = {
            "hdnDtaEdicao": data_edicao,
            "hdnTipoEdicao": "C",
            "hdnBolEdicaoGerada": "false",
            "hdnIdEdicao": "",
            "hdnInicio": "0",
            "hdnFormato": "json"
        }

        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        text = response.text[:-1]
        if len(text) > 300:
            json_data = json.loads(response.text[:-1])

            dados = pd.DataFrame(json_data['edicao'])
            dados = dados.query("unidade == 'SMUL/Unidade do Aprova Digital'")
            dados['data'] = data_edicao
            dados = dados.drop('link', axis=1)
            data_container.append(dados)
            print(f'DOM dia {data_edicao} - extraído')
        else:
            print(f'DOM dia {data_edicao} - não existe')

        # n seja abusivo
        time.sleep(2)

    df = pd.concat(data_container)
    df.to_csv(f'dom_{data_edicao[3:5]}.csv', index=False, sep=';', encoding='latin-1')
