/* =========================================
   NOVA ACADEMY
   Light / Dark Theme
   ========================================= */

(function () {

    const savedTheme = localStorage.getItem("nova-theme");

    const systemPrefersDark =
        window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: dark)").matches;


    // انتخاب تم اولیه
    if (savedTheme === "dark") {

        document.documentElement.setAttribute(
            "data-theme",
            "dark"
        );

    } else if (savedTheme === "light") {

        document.documentElement.setAttribute(
            "data-theme",
            "light"
        );

    } else if (systemPrefersDark) {

        document.documentElement.setAttribute(
            "data-theme",
            "dark"
        );

    } else {

        document.documentElement.setAttribute(
            "data-theme",
            "light"
        );

    }


    // وقتی صفحه کاملاً لود شد
    document.addEventListener("DOMContentLoaded", function () {

        const themeButton =
            document.querySelector(".theme-toggle");


        if (!themeButton) {
            return;
        }


        function updateButton() {

            const currentTheme =
                document.documentElement.getAttribute("data-theme");


            if (currentTheme === "dark") {

                themeButton.textContent = "☀️";

                themeButton.setAttribute(
                    "aria-label",
                    "Switch to light mode"
                );

                themeButton.setAttribute(
                    "title",
                    "Light Mode"
                );

            } else {

                themeButton.textContent = "🌙";

                themeButton.setAttribute(
                    "aria-label",
                    "Switch to dark mode"
                );

                themeButton.setAttribute(
                    "title",
                    "Dark Mode"
                );

            }

        }


        updateButton();


        themeButton.addEventListener("click", function () {

            const currentTheme =
                document.documentElement.getAttribute("data-theme");


            const newTheme =
                currentTheme === "dark"
                    ? "light"
                    : "dark";


            document.documentElement.setAttribute(
                "data-theme",
                newTheme
            );


            localStorage.setItem(
                "nova-theme",
                newTheme
            );


            updateButton();

        });

    });

})();