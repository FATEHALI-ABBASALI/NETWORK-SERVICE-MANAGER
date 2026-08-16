<div align="center">

# 🌐 Network Service Manager

### 🐧 Linux Network Service Management GUI

<p>
A Python-based GUI application for managing supported network services on Debian-based Linux systems.
</p>

<p>
<b>Ubuntu • Kali Linux • Debian • Python 3</b>
</p>

</div>

<hr>

<h2>📌 About</h2>

<p>
<strong>Network Service Manager</strong> is a simple and user-friendly GUI application developed in Python for managing supported Linux network services.
</p>

<p>
The project is mainly designed for <strong>Ubuntu, Kali Linux and other Debian-based Linux distributions</strong>. It helps users perform network-service operations through a graphical interface instead of entering every command manually.
</p>

<h2>✨ Features</h2>

<ul>
  <li>🖥️ Simple GUI interface</li>
  <li>🌐 Network service management</li>
  <li>▶️ Start services</li>
  <li>⏹️ Stop services</li>
  <li>🔄 Restart services</li>
  <li>🔐 Administrator/root operations</li>
  <li>🐍 Python virtual environment support</li>
</ul>

<hr>

<h2>💻 Requirements</h2>

<ul>
  <li>🐧 Ubuntu / Kali Linux / Debian-based Linux</li>
  <li>🐍 Python 3</li>
  <li>📦 pip</li>
  <li>📦 python3-venv</li>
  <li>🌐 Git</li>
</ul>

<hr>

<h2>🚀 Installation & Setup</h2>

<p>Follow these steps in order.</p>

<h3>1️⃣ Update Linux</h3>

<p>Open the terminal and run:</p>

<pre><code>sudo apt update</code></pre>

<h3>2️⃣ Install Required Packages</h3>

<pre><code>sudo apt install python3 python3-pip python3-venv git -y</code></pre>

<p>Check Python:</p>

<pre><code>python3 --version</code></pre>

<p>Check pip:</p>

<pre><code>pip3 --version</code></pre>

<hr>

<h2>📥 3️⃣ Download the Project</h2>

<p>Clone the repository:</p>

<pre><code>git clone https://github.com/FATEHALI-ABBASALI/NETWORK-SERVICE-MANAGER.git</code></pre>

<p>Go inside the project:</p>

<pre><code>cd network-service-manager</code></pre>

<p>Your terminal should now be inside the project folder.</p>

<hr>

<h2>🐍 4️⃣ Create Python Virtual Environment</h2>

<p>
A virtual environment keeps the project's Python packages separate from the system Python.
</p>

<pre><code>python3 -m venv venv</code></pre>

<p>This creates a folder:</p>

<pre><code>venv/</code></pre>

<hr>

<h2>▶️ 5️⃣ Activate Virtual Environment</h2>

<p>Run:</p>

<pre><code>source venv/bin/activate</code></pre>

<p>
After successful activation, you will see <strong>(venv)</strong> at the beginning of the terminal.
</p>

<pre>
(venv) user@ubuntu:~/network-service-manager$
</pre>

<p>
<strong>Important:</strong> Activate the virtual environment before installing project requirements or running the application.
</p>

<hr>

<h2>📦 6️⃣ Install Requirements</h2>

<p>
The <code>requirements.txt</code> file contains the Python packages required by the project.
</p>

<p>With the virtual environment active, run:</p>

<pre><code>pip install -r requirements.txt</code></pre>

<p>To check installed packages:</p>

<pre><code>pip list</code></pre>

<hr>

<h2>▶️ 7️⃣ Run the Application</h2>

<p>
After completing the previous steps, start the application using:
</p>

<pre><code>python3 main.py</code></pre>

<p>On systems where <code>python</code> points to Python 3, you can also use:</p>

<pre><code>python main.py</code></pre>

<p>
The <strong>Network Service Manager GUI</strong> should now open.
</p>

<hr>

<h2>🔐 8️⃣ Run With Administrator Privileges</h2>

<p>
Some network-service operations require administrator privileges.
</p>

<p>You can switch to the root user:</p>

<pre><code>sudo su</code></pre>

<p>Then go to the project folder:</p>

<pre><code>cd /path/to/network-service-manager</code></pre>

<p>Activate the virtual environment:</p>

<pre><code>source venv/bin/activate</code></pre>

<p>Run the application:</p>

<pre><code>python3 main.py</code></pre>

<p>
Alternatively, if root access is not already active:
</p>

<pre><code>sudo python3 main.py</code></pre>

<p>
<strong>⚠️ Note:</strong> Use administrator privileges only when required by the network-service operation.
</p>

<hr>

<h2>⚡ Complete Setup in One Go</h2>

<p>
If Python and Git are already installed, the basic setup is:
</p>

<pre><code>git clone https://github.com/FATEHALI-ABBASALI/NETWORK-SERVICE-MANAGER.git;
cd network-service-manager

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python3 main.py</code></pre>

<hr>

<h2>🔄 Next Time You Run the Project</h2>

<p>
You do not need to create the virtual environment again. Just open the terminal and run:
</p>

<pre><code>cd network-service-manager
source venv/bin/activate
python3 main.py</code></pre>

<p>
If administrator privileges are required:
</p>

<pre><code>sudo python3 main.py</code></pre>

<hr>

<h2>🛑 Stop / Deactivate</h2>

<p>
When you finish working with the project, deactivate the virtual environment:
</p>

<pre><code>deactivate</code></pre>

<hr>

<h2>🔧 Troubleshooting</h2>

<h3>❌ Python not found</h3>

<pre><code>sudo apt install python3 -y</code></pre>

<h3>❌ pip not found</h3>

<pre><code>sudo apt install python3-pip -y</code></pre>

<h3>❌ venv error</h3>

<pre><code>sudo apt install python3-venv -y</code></pre>

<p>Then create the environment again:</p>

<pre><code>python3 -m venv venv</code></pre>

<h3>❌ Permission denied</h3>

<p>Try running with administrator privileges:</p>

<pre><code>sudo python3 main.py</code></pre>

<h3>❌ Requirements installation failed</h3>

<p>Make sure <code>(venv)</code> is visible in your terminal:</p>

<pre><code>source venv/bin/activate</code></pre>

<p>Then run:</p>

<pre><code>pip install -r requirements.txt</code></pre>

<hr>

<h2>📁 Project Structure</h2>

<pre>
network-service-manager/
│
├── app/
│   ├── services/
│   │   ├── command_runner.py
│   │   └── service_manager.py
│   │
│   ├── ui/
│   │   └── main_window.py
│   │
│   └── utils/
│       ├── constants.py
│       └── platform.py
│
├── venv/
├── requirements.txt
├── main.py
└── README.md
</pre>

<hr>

<h2>⚙️ Linux Service Commands</h2>

<p>
The application works with Linux service-management operations such as:
</p>

<pre><code>sudo systemctl start &lt;service&gt;
sudo systemctl stop &lt;service&gt;
sudo systemctl restart &lt;service&gt;
sudo systemctl status &lt;service&gt;</code></pre>

<p>
The GUI provides an easier way to perform supported operations.
</p>

<hr>

<h2>🎓 Project Purpose</h2>

<p>
This project is created for learning and practical understanding of:
</p>

<ul>
  <li>🌐 Computer Networking</li>
  <li>🐧 Linux Administration</li>
  <li>⚙️ Network Services</li>
  <li>🐍 Python Programming</li>
  <li>🖥️ GUI Development</li>
  <li>🔐 Linux Permissions</li>
  <li>📦 Python Virtual Environments</li>
</ul>

<hr>

<h2>⚠️ Important</h2>

<ul>
  <li>Use this application only on systems you own or are authorized to manage.</li>
  <li>Some operations require administrator privileges.</li>
  <li>The project is mainly intended for Debian-based Linux systems.</li>
</ul>

<hr>

<div align="center">

<h3>🌐 Network Service Manager</h3>

<p>
<b>Python • Linux • Networking</b>
</p>

</div>
