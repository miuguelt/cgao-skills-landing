tailwind.config = {
    theme: {
        extend: {
            colors: {
                'neon-green': '#39FF14',
                'amber-gold': '#FFBF00',
                'slate-950': '#0a0a0f',
            },
            fontFamily: {
                'inter': ['Inter', 'sans-serif'],
            },
            animation: {
                'glow': 'glow 2s ease-in-out infinite alternate',
                'float': 'float 6s ease-in-out infinite',
                'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'slide-up': 'slideUp 0.8s ease-out forwards',
                'fade-in': 'fadeIn 1s ease-out forwards',
            },
            keyframes: {
                glow: {
                    '0%': { boxShadow: '0 0 20px #39FF14, 0 0 40px #39FF14, 0 0 60px #39FF14' },
                    '100%': { boxShadow: '0 0 30px #FFBF00, 0 0 50px #FFBF00, 0 0 70px #FFBF00' },
                },
                float: {
                    '0%, 100%': { transform: 'translateY(0px)' },
                    '50%': { transform: 'translateY(-20px)' },
                },
                slideUp: {
                    '0%': { opacity: '0', transform: 'translateY(50px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
                fadeIn: {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                },
            }
        }
    }
}
