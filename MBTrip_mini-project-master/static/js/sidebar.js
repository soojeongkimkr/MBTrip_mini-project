// 사이드바
        /* EXPANDER MENU */
        const showMenu = (toggleId, navbarId, bodyId) => {
            const toggle = document.getElementById(toggleId),
                navbar = document.getElementById(navbarId),
                bodypadding = document.getElementById(bodyId)

            if (toggle && navbar) {
                toggle.addEventListener('click', () => {
                    navbar.classList.toggle('expander');

                    bodypadding.classList.toggle('body-pd')
                })
            }
        }

        showMenu('nav-toggle', 'navbar', 'body-pd')

        const headerTitle = document.getElementsByClassName('title')
        const btn= document.createElelment("button");
        const t = document.createTextNode("로그인으로 가기");
        const button = btn.appendChild(t);
        headerTitle.append(button)
