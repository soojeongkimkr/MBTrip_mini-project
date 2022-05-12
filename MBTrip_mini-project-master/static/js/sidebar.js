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

const headerTitle = document.querySelector('.header .title')
  // 1. <div> element 만들기
  const newDiv = document.createElement('div');
  
  // 2. <div>에 들어갈 text node 만들기
  const newText = document.createTextNode('로그인으로 이동');
  
  // 3. <div>에 text node 붙이기
  newDiv.appendChild(newText);
  
  // 4. <body>에 1에서 만든 <div> element 붙이기
  headerTitle.appendChild(newDiv);
    
  newDiv.className='button'
  newDiv.style.cssText='width:110px; font-size:12px;height:30px;border-radius: 5px; border:1px solid #fff; display:flex; cursor:pointer; justify-content: center; align-items: center;'

