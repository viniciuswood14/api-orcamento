from fastapi import FastAPI, HTTPException
from orcamentobr import despesa_detalhada
import pandas as pd
from typing import Optional

# Cria a aplicação FastAPI
app = FastAPI(
    title="API de Consulta ao Orçamento Federal",
    description="Um wrapper de API para a biblioteca orcamentobr."
)

@app.get("/")
def ler_raiz():
    return {"status": "API online", "documentacao": "/docs"}

@app.get("/consulta-despesa/")
async def consultar_despesa(
    ano: int, 
    funcao: Optional[str] = None, 
    orgao: Optional[str] = None,
    acao: Optional[str] = None
):
    """
    Endpoint para consultar despesas detalhadas.
    Exemplo: /consulta-despesa/?ano=2023&funcao=04
    """
    print(f"Recebida consulta para ano={ano}, funcao={funcao}, orgao={orgao}, acao={acao}")

    try:
        # Chama a biblioteca 'orcamentobr'
        dados_df = despesa_detalhada(
            exercicio=ano,
            funcao=funcao if funcao else False,
            orgao=orgao if orgao else False,
            acao=acao if acao else False,
            inclui_descricoes=True
        )

        if dados_df.empty:
            return {"mensagem": "Nenhum dado encontrado para esta consulta."}

        # Converte o resultado (Pandas DataFrame) para JSON
        dados_json = dados_df.to_dict("records")
        return dados_json

    except Exception as e:
        print(f"Erro ao processar consulta: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno ao consultar o orçamento: {str(e)}")
