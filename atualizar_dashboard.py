"""
Script de automação para atualizar dados do Dashboard de Retorno
Copia arquivos atualizados e faz push para o GitHub
"""

import shutil
import subprocess
import os
from datetime import datetime
from pathlib import Path

# Configurações
DASHBOARD_DIR = Path(__file__).parent
PASTA_ORIGEM = DASHBOARD_DIR.parent

ARQUIVOS_PARA_ATUALIZAR = [
    "historico_envios.json",
    "Vendas_Lubrimax.xlsx"
]

def log(mensagem):
    """Registra mensagem com timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {mensagem}")

def copiar_arquivos():
    """Copia arquivos atualizados da pasta origem"""
    log("Iniciando cópia de arquivos...")
    
    for arquivo in ARQUIVOS_PARA_ATUALIZAR:
        origem = PASTA_ORIGEM / arquivo
        destino = DASHBOARD_DIR / arquivo
        
        if origem.exists():
            shutil.copy2(origem, destino)
            log(f"✅ {arquivo} copiado com sucesso")
        else:
            log(f"⚠️ {arquivo} não encontrado em {origem}")
    
    log("Cópia concluída!")

def git_commit_push():
    """Faz commit e push das alterações"""
    log("Verificando alterações no Git...")
    
    os.chdir(DASHBOARD_DIR)
    
    # Verifica se há alterações
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True
    )
    
    if not result.stdout.strip():
        log("ℹ️ Nenhuma alteração para commitar")
        return
    
    # Adiciona arquivos
    log("Adicionando arquivos...")
    subprocess.run(["git", "add"] + ARQUIVOS_PARA_ATUALIZAR, check=True)
    
    # Commit
    mensagem = f"Auto-update: dados atualizados em {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    log(f"Fazendo commit: {mensagem}")
    result_commit = subprocess.run(
        ["git", "commit", "-m", mensagem],
        capture_output=True,
        text=True
    )
    
    if result_commit.returncode != 0:
        log("ℹ️ Nenhuma alteração para commitar")
        return
    
    # Push
    log("Enviando para GitHub...")
    subprocess.run(["git", "push"], check=True)
    
    log("✅ Push realizado com sucesso!")

def main():
    """Função principal"""
    log("="*60)
    log("INICIANDO ATUALIZAÇÃO DO DASHBOARD")
    log("="*60)
    
    try:
        copiar_arquivos()
        git_commit_push()
        log("="*60)
        log("✅ ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!")
        log("="*60)
    except Exception as e:
        log("="*60)
        log(f"❌ ERRO: {str(e)}")
        log("="*60)
        raise

if __name__ == "__main__":
    main()
