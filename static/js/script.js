// Script principal do Sistema de Certificados NR

// Configurações globais
const CONFIG = {
    animationDuration: 300,
    toastDuration: 5000,
    apiTimeout: 30000
};

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Função principal de inicialização
function initializeApp() {
    initializeTooltips();
    initializeAnimations();
    initializeFormValidations();
    initializeUtilities();
    setupGlobalEvents();
}

// Inicializar tooltips do Bootstrap
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Inicializar animações
function initializeAnimations() {
    // Fade in para cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Validações de formulário
function initializeFormValidations() {
    // Validação de CPF em tempo real
    const cpfInputs = document.querySelectorAll('input[name="cpf"]');
    cpfInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            // Aplicar máscara
            if (value.length <= 11) {
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
                value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
                e.target.value = value;
            }
            
            // Validar CPF
            if (value.replace(/\D/g, '').length === 11) {
                if (validarCPF(value)) {
                    e.target.classList.remove('is-invalid');
                    e.target.classList.add('is-valid');
                } else {
                    e.target.classList.remove('is-valid');
                    e.target.classList.add('is-invalid');
                }
            } else {
                e.target.classList.remove('is-valid', 'is-invalid');
            }
        });
    });
    
    // Validação de campos obrigatórios
    const requiredInputs = document.querySelectorAll('input[required], select[required], textarea[required]');
    requiredInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateRequiredField(this);
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('is-invalid')) {
                validateRequiredField(this);
            }
        });
    });
}

// Utilitários gerais
function initializeUtilities() {
    // Auto-resize para textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    });
    
    // Formatação automática de datas
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        if (!input.value) {
            input.value = new Date().toISOString().split('T')[0];
        }
    });
}

// Eventos globais
function setupGlobalEvents() {
    // Confirmação para ações destrutivas
    const deleteButtons = document.querySelectorAll('.btn-danger, [onclick*="excluir"], [onclick*="delete"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja excluir este item?')) {
                e.preventDefault();
                e.stopPropagation();
            }
        });
    });
    
    // Loading para formulários
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                showLoadingButton(submitBtn);
            }
        });
    });
}

// Função para validar CPF
function validarCPF(cpf) {
    cpf = cpf.replace(/[^\d]+/g, '');
    
    if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) {
        return false;
    }
    
    let soma = 0;
    for (let i = 0; i < 9; i++) {
        soma += parseInt(cpf.charAt(i)) * (10 - i);
    }
    
    let resto = 11 - (soma % 11);
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpf.charAt(9))) return false;
    
    soma = 0;
    for (let i = 0; i < 10; i++) {
        soma += parseInt(cpf.charAt(i)) * (11 - i);
    }
    
    resto = 11 - (soma % 11);
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpf.charAt(10))) return false;
    
    return true;
}

// Validar campo obrigatório
function validateRequiredField(field) {
    if (field.value.trim() === '') {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
        return false;
    } else {
        field.classList.add('is-valid');
        field.classList.remove('is-invalid');
        return true;
    }
}

// Mostrar loading em botão
function showLoadingButton(button) {
    const originalText = button.innerHTML;
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Processando...';
    
    // Restaurar após 30 segundos se não houver redirecionamento
    setTimeout(() => {
        button.disabled = false;
        button.innerHTML = originalText;
    }, 30000);
}

// Toast notifications
function showToast(message, type = 'info', duration = CONFIG.toastDuration) {
    const toastContainer = getOrCreateToastContainer();
    
    const toastId = 'toast-' + Date.now();
    const iconClass = {
        'success': 'fas fa-check-circle text-success',
        'error': 'fas fa-exclamation-triangle text-danger',
        'warning': 'fas fa-exclamation-circle text-warning',
        'info': 'fas fa-info-circle text-info'
    }[type] || 'fas fa-info-circle text-info';
    
    const toastHTML = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="${duration}">
            <div class="toast-header">
                <i class="${iconClass} me-2"></i>
                <strong class="me-auto">Sistema de Certificados</strong>
                <small class="text-muted">agora</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remover do DOM após fechar
    toastElement.addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

// Obter ou criar container de toasts
function getOrCreateToastContainer() {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    return container;
}

// Função para confirmar ações
function confirmarAcao(titulo, texto, callback) {
    Swal.fire({
        title: titulo,
        text: texto,
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sim, continuar',
        cancelButtonText: 'Cancelar',
        confirmButtonColor: '#0d6efd',
        cancelButtonColor: '#6c757d'
    }).then((result) => {
        if (result.isConfirmed && typeof callback === 'function') {
            callback();
        }
    });
}

// Função para mostrar loading
function showLoading(titulo = 'Processando...', texto = 'Por favor, aguarde') {
    Swal.fire({
        title: titulo,
        text: texto,
        allowOutsideClick: false,
        allowEscapeKey: false,
        showConfirmButton: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });
}

// Função para ocultar loading
function hideLoading() {
    Swal.close();
}

// Função para mostrar sucesso
function showSuccess(titulo, texto = '') {
    Swal.fire({
        icon: 'success',
        title: titulo,
        text: texto,
        confirmButtonColor: '#198754'
    });
}

// Função para mostrar erro
function showError(titulo, texto = '') {
    Swal.fire({
        icon: 'error',
        title: titulo,
        text: texto,
        confirmButtonColor: '#dc3545'
    });
}

// Função para formatar data brasileira
function formatDateBR(date) {
    if (!date) return '';
    const d = new Date(date);
    return d.toLocaleDateString('pt-BR');
}

// Função para formatar CPF
function formatCPF(cpf) {
    if (!cpf) return '';
    const cleaned = cpf.replace(/\D/g, '');
    if (cleaned.length === 11) {
        return cleaned.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
    }
    return cpf;
}

// Função para debounce (otimização de performance)
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

// Função para salvar dados no localStorage
function saveToLocalStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
        return true;
    } catch (e) {
        console.error('Erro ao salvar no localStorage:', e);
        return false;
    }
}

// Função para carregar dados do localStorage
function loadFromLocalStorage(key) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    } catch (e) {
        console.error('Erro ao carregar do localStorage:', e);
        return null;
    }
}

// Função para exportar dados
function exportarDados(dados, nomeArquivo, tipo = 'json') {
    let content, mimeType, extension;
    
    switch (tipo) {
        case 'csv':
            content = jsonToCSV(dados);
            mimeType = 'text/csv';
            extension = '.csv';
            break;
        case 'json':
        default:
            content = JSON.stringify(dados, null, 2);
            mimeType = 'application/json';
            extension = '.json';
            break;
    }
    
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = nomeArquivo + extension;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Converter JSON para CSV
function jsonToCSV(jsonData) {
    if (!Array.isArray(jsonData) || jsonData.length === 0) {
        return '';
    }
    
    const headers = Object.keys(jsonData[0]);
    const csvHeaders = headers.join(',');
    
    const csvRows = jsonData.map(row => {
        return headers.map(header => {
            const value = row[header] || '';
            return `"${value.toString().replace(/"/g, '""')}"`;
        }).join(',');
    });
    
    return [csvHeaders, ...csvRows].join('\n');
}

// Função para imprimir página
function imprimirPagina() {
    window.print();
}

// Função para copiar texto para clipboard
function copiarParaClipboard(texto) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(texto).then(() => {
            showToast('Texto copiado para a área de transferência', 'success');
        }).catch(() => {
            showToast('Erro ao copiar texto', 'error');
        });
    } else {
        // Fallback para navegadores mais antigos
        const textArea = document.createElement('textarea');
        textArea.value = texto;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            showToast('Texto copiado para a área de transferência', 'success');
        } catch {
            showToast('Erro ao copiar texto', 'error');
        }
        document.body.removeChild(textArea);
    }
}

// Função para verificar conexão com internet
function verificarConexao() {
    return navigator.onLine;
}

// Event listeners para conexão
window.addEventListener('online', function() {
    showToast('Conexão restaurada', 'success');
});

window.addEventListener('offline', function() {
    showToast('Sem conexão com a internet', 'warning');
});

// Função para validar email
function validarEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

// Função para validar telefone brasileiro
function validarTelefone(telefone) {
    const regex = /^(\+55|55)?\s?(\(?\d{2}\)?)?\s?(\d{4,5})-?(\d{4})$/;
    return regex.test(telefone);
}

// Função para gerar ID único
function gerarId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

// Exportar funções globais para uso em outros scripts
window.SistemaCertificados = {
    validarCPF,
    formatCPF,
    formatDateBR,
    showToast,
    confirmarAcao,
    showLoading,
    hideLoading,
    showSuccess,
    showError,
    exportarDados,
    copiarParaClipboard,
    imprimirPagina,
    verificarConexao,
    validarEmail,
    validarTelefone,
    gerarId,
    debounce,
    saveToLocalStorage,
    loadFromLocalStorage
};

console.log('Sistema de Certificados NR carregado com sucesso!');
