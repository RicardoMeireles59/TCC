document.addEventListener('DOMContentLoaded', () => {

    // --- SISTEMA DE TEMA (DARK/LIGHT MODE) ---
    // Verifica se o usuário já salvou preferência de tema antes
    const savedTheme = localStorage.getItem('easyEnglish_theme') || 'dark';
    if (savedTheme === 'light') {
        document.body.classList.add('light-theme');
    }

    // Cria a função global para alternar o tema
    window.toggleTheme = function() {
        document.body.classList.toggle('light-theme');
        const isLight = document.body.classList.contains('light-theme');
        localStorage.setItem('easyEnglish_theme', isLight ? 'light' : 'dark');
    };

    // --- NAVEGAÇÃO DE TELAS ---
    const screenLogin = document.getElementById('screen-login');
    const screenRegister = document.getElementById('screen-register');
    const screenDashboard = document.getElementById('screen-dashboard');

    const linkToRegister = document.getElementById('link-to-register');
    const linkToLogin = document.getElementById('link-to-login');

    // Funções de troca de tela
    function showScreen(screen) {
        screenLogin.classList.add('hidden');
        screenRegister.classList.add('hidden');
        screenDashboard.classList.add('hidden');
        screen.classList.remove('hidden');
    }

    linkToRegister.addEventListener('click', (e) => {
        e.preventDefault();
        // Limpa erros visuais residuais ao mudar de tela
        document.querySelectorAll('input').forEach(input => clearError(input));
        showScreen(screenRegister);
    });

    linkToLogin.addEventListener('click', (e) => {
        e.preventDefault();
        // Limpa erros visuais residuais ao mudar de tela
        document.querySelectorAll('input').forEach(input => clearError(input));
        showScreen(screenLogin);
    });

    // Atualiza o nome de boas-vindas dinamicamente no Dashboard
    function updateDashboardName(name) {
        const welcomeHeader = document.querySelector('.welcome-section h2');
        if (welcomeHeader) {
            const firstName = name.split(' ')[0];
            welcomeHeader.innerText = `Olá, ${firstName}! ✨`;
        }
    }

    // --- SISTEMA DE NOTIFICAÇÃO TOAST ---
    const toastNotification = document.getElementById('toast-notification');

    function showToast(message, type = 'success') {
        toastNotification.innerHTML = type === 'success' 
            ? `✅ ${message}` 
            : `❌ ${message}`;
        
        toastNotification.className = `toast ${type} show-toast`;

        // Esconde o Toast automaticamente após 4 segundos
        setTimeout(() => {
            toastNotification.classList.remove('show-toast');
        }, 4000);
    }

    // --- SISTEMA DE VALIDAÇÃO VISUAL (Inline Erros) ---
    function showError(inputElement, message) {
        clearError(inputElement); 
        inputElement.classList.add('input-error');
        const errorSpan = document.createElement('span');
        errorSpan.className = 'error-text';
        errorSpan.innerText = message;
        inputElement.parentNode.insertBefore(errorSpan, inputElement.nextSibling);
    }

    function clearError(inputElement) {
        inputElement.classList.remove('input-error');
        const nextSibling = inputElement.nextElementSibling;
        if (nextSibling && nextSibling.classList.contains('error-text')) {
            nextSibling.remove();
        }
    }

    // Validação de E-mail via RegEx
    function isValidEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }

    // Limpa os erros em tempo real assim que o usuário digita nos campos
    document.querySelectorAll('input').forEach(input => {
        input.addEventListener('input', function() {
            clearError(this);
            // Se estiver na tela de login, limpa o erro mútuo de senha ao digitar no e-mail
            if (this.id === 'login-email' || this.id === 'login-password') {
                clearError(document.getElementById('login-password'));
                clearError(document.getElementById('login-email'));
            }
        });
    });

    // --- LOGICA DE CADASTRO (Gravação Local) ---
    document.getElementById('btn-register-submit').addEventListener('click', () => {
        const nameInput = document.getElementById('reg-name');
        const lastnameInput = document.getElementById('reg-lastname');
        const emailInput = document.getElementById('reg-email');
        const passInput = document.getElementById('reg-password');
        const confirmPassInput = document.getElementById('reg-confirm');
        const termsCheckbox = document.getElementById('reg-terms');
        
        let isValid = true;

        if (!nameInput.value.trim()) { showError(nameInput, 'Nome obrigatório.'); isValid = false; }
        if (!lastnameInput.value.trim()) { showError(lastnameInput, 'Sobrenome obrigatório.'); isValid = false; }
        
        if (!emailInput.value.trim()) {
            showError(emailInput, 'E-mail obrigatório.'); isValid = false;
        } else if (!isValidEmail(emailInput.value.trim())) {
            showError(emailInput, 'Formato de e-mail inválido.'); isValid = false;
        }

        if (passInput.value.length < 6) {
            showError(passInput, 'A senha deve ter pelo menos 6 caracteres.'); isValid = false;
        }

        if (!confirmPassInput.value.trim()) {
            showError(confirmPassInput, 'Confirme sua senha.'); isValid = false;
        } else if (confirmPassInput.value !== passInput.value) {
            showError(confirmPassInput, 'As senhas não coincidem.'); isValid = false;
        }

        const termsLabel = document.querySelector('label[for="reg-terms"]');
        if (!termsCheckbox.checked) {
            // Alterado de '#ff4a4a' para utilizar a variável do design system
            termsLabel.style.color = 'var(--status-error)'; isValid = false;
        } else {
            // Alterado de '#777' para a variável do design system
            termsLabel.style.color = 'var(--text-muted)'; 
        }

        termsCheckbox.addEventListener('change', function() {
            if (this.checked) termsLabel.style.color = 'var(--text-muted)';
        });

        // Se o formulário estiver correto, persiste no localStorage
        if (isValid) {
            const userData = {
                name: nameInput.value.trim(),
                email: emailInput.value.trim().toLowerCase(),
                password: passInput.value
            };

            // Guarda os dados no navegador convertidos em String JSON
            localStorage.setItem('easyEnglish_user', JSON.stringify(userData));
            
            // Limpa o formulário de cadastro completamente
            document.querySelectorAll('#screen-register input:not([type="checkbox"])').forEach(input => input.value = '');
            termsCheckbox.checked = false;

            // Retorna à tela de login, preenche o e-mail cadastrado e dispara a notificação
            showScreen(screenLogin);
            document.getElementById('login-email').value = userData.email;
            showToast('Conta criada com sucesso! Faça seu login.', 'success');
        }
    });

    // --- LÓGICA DE LOGIN (Validação de Credenciais Real) ---
    document.getElementById('btn-login-submit').addEventListener('click', () => {
        const emailInput = document.getElementById('login-email');
        const passInput = document.getElementById('login-password');
        let isValid = true;

        if (!emailInput.value.trim()) {
            showError(emailInput, 'Por favor, insira seu e-mail.'); isValid = false;
        } else if (!isValidEmail(emailInput.value.trim())) {
            showError(emailInput, 'Insira um formato de e-mail válido.'); isValid = false;
        }

        if (!passInput.value.trim()) {
            showError(passInput, 'A senha é obrigatória.'); isValid = false;
        }

        // Se a validação dos campos passou, checa no localStorage
        if (isValid) {
            const userEmail = emailInput.value.trim().toLowerCase();
            const userPass = passInput.value;
            
            // Puxa a string do localStorage e converte de volta para objeto
            const savedDataString = localStorage.getItem('easyEnglish_user');
            
            if (!savedDataString) {
                showError(emailInput, 'Nenhuma conta encontrada. Cadastre-se primeiro!');
                return;
            }

            const savedUser = JSON.parse(savedDataString);

            // Valida se as credenciais digitadas batem com o cadastro salvo
            if (savedUser.email !== userEmail) {
                showError(emailInput, 'E-mail não encontrado.');
            } else if (savedUser.password !== userPass) {
                showError(passInput, 'Senha incorreta. Tente novamente.');
            } else {
                // Credenciais corretas! Limpa campos e entra
                emailInput.value = '';
                passInput.value = '';
                
                updateDashboardName(savedUser.name);
                showScreen(screenDashboard);
                showToast('Login realizado com sucesso!', 'success');
            }
        }
    });
});