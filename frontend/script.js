const runBtn = document.getElementById('runBtn');
const clearBtn = document.getElementById('clearBtn');
const pg = document.getElementById('pg');
const output = document.getElementById('output');
const copyBtn = document.getElementById('cp');

runBtn.addEventListener('click', async () => {
    const code = pg.value;
    if (!code) {
        output.textContent = 'Please enter some code to run.';
        return;
    }

    output.textContent = 'Running...';

    try {
        const res = await fetch('https://junklangweb.onrender.com/run', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code })
        });

        if (!res.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await res.json();
        output.textContent = data.output;
    } catch (error) {
        output.textContent = `Error: ${error.message}`;
        console.error('Error running code:', error);
    }
});

clearBtn.addEventListener('click', () => {
    pg.value = '';
    output.textContent = 'Output will appear here...';
});

function copy() {
    const text = "pip install junklang";
    navigator.clipboard.writeText(text).then(() => {
        const copyButton = document.getElementById('cp');
        copyButton.innerHTML = '<i class="fa-solid fa-square-check"></i>';
        setTimeout(() => {
            copyButton.innerHTML = '<i class="fa fa-copy"></i>';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy: ', err);
    });
}

copyBtn.addEventListener('click', copy);