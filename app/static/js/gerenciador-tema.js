/**
 * Gerenciador de Temas
 * Script para controlar a alternância entre tema claro e escuro
 */

(function() {
    // Constantes para os temas
    const TEMA_CLARO = 'tema-claro';
    const TEMA_ESCURO = 'tema-escuro';
    const TEMA_CHAVE = 'autoita-tema-preferido';
    
    // Elementos DOM
    const btnTema = document.getElementById('botao-tema');
    const temaAtual = document.getElementById('tema-atual');
    const iconeTemaBotao = btnTema ? btnTema.querySelector('span.fas') : null;
    const textoTemaBotao = btnTema ? btnTema.querySelector('.texto-tema') : null;
    
    // Detecta se o sistema do usuário prefere tema escuro
    const prefereEscuro = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Obtém o tema dos cookies ou usa o padrão baseado na preferência do sistema
    const getTemaAtual = () => {
        const temaSalvo = localStorage.getItem(TEMA_CHAVE);
        return temaSalvo || (prefereEscuro ? TEMA_ESCURO : TEMA_CLARO);
    };
    
    // Aplica um tema específico
    const aplicarTema = (tema) => {
        if (!temaAtual) return;
        
        // Atualiza o link de CSS
        temaAtual.href = `/static/css/temas/${tema}.css`;
        
        // Atualiza o ícone e texto do botão
        if (iconeTemaBotao && textoTemaBotao) {
            if (tema === TEMA_ESCURO) {
                iconeTemaBotao.classList.remove('fa-moon');
                iconeTemaBotao.classList.add('fa-sun');
                textoTemaBotao.textContent = 'Tema Claro';
            } else {
                iconeTemaBotao.classList.remove('fa-sun');
                iconeTemaBotao.classList.add('fa-moon');
                textoTemaBotao.textContent = 'Tema Escuro';
            }
        }
        
        // Adiciona classes ao data-theme no HTML para permitir estilizações específicas
        document.documentElement.setAttribute('data-theme', tema);
        
        // Salva a preferência do usuário
        localStorage.setItem(TEMA_CHAVE, tema);
        
        // Dispara um evento personalizado para notificar outros scripts
        document.dispatchEvent(new CustomEvent('temaAlterado', { detail: { tema } }));
    };
    
    // Alternar entre os temas
    const alternarTema = () => {
        const temaAtual = getTemaAtual();
        const novoTema = temaAtual === TEMA_CLARO ? TEMA_ESCURO : TEMA_CLARO;
        aplicarTema(novoTema);
        
        // Adiciona animação sutil de transição na página
        document.body.classList.add('tema-transicao');
        setTimeout(() => {
            document.body.classList.remove('tema-transicao');
        }, 300);
    };
    
    // Inicializa o tema
    const inicializarTema = () => {
        // Aplica o tema inicial
        aplicarTema(getTemaAtual());
        
        // Adiciona o listener para o botão de alternar tema
        if (btnTema) {
            btnTema.addEventListener('click', alternarTema);
        }
        
        // Escuta por mudanças na preferência do sistema
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
                if (!localStorage.getItem(TEMA_CHAVE)) {
                    // Se o usuário não salvou uma preferência, siga o sistema
                    aplicarTema(e.matches ? TEMA_ESCURO : TEMA_CLARO);
                }
            });
        }
        
        // Adiciona classe para habilitar transições após o carregamento
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => {
                document.body.classList.add('transicoes-ativas');
            }, 300);
        });
    };
    
    // Inicia o script
    inicializarTema();
})();