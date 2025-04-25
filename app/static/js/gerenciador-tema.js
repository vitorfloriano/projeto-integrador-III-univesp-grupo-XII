/**
 * Gerenciador de Tema
 * Script para gerenciar a alternância entre tema claro e escuro
 */

document.addEventListener('DOMContentLoaded', function() {
    // Função para aplicar o tema
    function aplicarTema(tema) {
        // Caminho base para os arquivos CSS
        const baseUrl = '/static/css/temas/';
        
        // Define o caminho do arquivo de tema
        const temaCssUrl = `${baseUrl}tema-${tema}.css`;
        
        // Atualiza o link de referência CSS
        let linkTema = document.getElementById('link-tema');
        if (linkTema) {
            linkTema.href = temaCssUrl;
        } else {
            // Se o link ainda não existe, cria um novo
            const novoLink = document.createElement('link');
            novoLink.rel = 'stylesheet';
            novoLink.id = 'link-tema';
            novoLink.href = temaCssUrl;
            document.head.appendChild(novoLink);
        }
        
        // Atualiza o ícone e texto do botão
        const iconeTema = document.querySelector('.botao-tema span:first-child');
        const textoTema = document.querySelector('.texto-tema');
        
        if (iconeTema && textoTema) {
            if (tema === 'escuro') {
                iconeTema.className = 'fas fa-sun';
                textoTema.textContent = 'Tema Claro';
                document.body.classList.add('tema-escuro');
                document.body.classList.remove('tema-claro');
            } else {
                iconeTema.className = 'fas fa-moon';
                textoTema.textContent = 'Tema Escuro';
                document.body.classList.add('tema-claro');
                document.body.classList.remove('tema-escuro');
            }
        }
        
        // Salva a preferência do usuário
        localStorage.setItem('tema', tema);
    }
    
    const botaoTema = document.querySelector('.botao-tema');
    
    // Verifica o tema atual armazenado (ou usa claro como padrão)
    const temaInicial = localStorage.getItem('tema') || 'claro';
    
    // Aplica o tema inicial
    aplicarTema(temaInicial);
    
    // Adiciona evento de clique no botão de tema
    if (botaoTema) {
        botaoTema.addEventListener('click', function() {
            // Obtém o tema atual antes de alternar
            const temaAtual = localStorage.getItem('tema') || 'claro';
            // Alterna entre temas claro e escuro
            const novoTema = temaAtual === 'claro' ? 'escuro' : 'claro';
            aplicarTema(novoTema);
        });
    }
});