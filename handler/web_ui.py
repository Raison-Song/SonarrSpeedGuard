import json
from typing import Dict, Tuple, List, Optional

from flask import Blueprint, render_template_string, request

import utils.config

main_routes = Blueprint('main', __name__)


@main_routes.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    category = ""
    if request.method == 'POST':
        apikey = request.form.get('apikey', '').strip()
        host = request.form.get('host', '').strip()
        port = request.form.get('port', '8989').strip()
        ssl = request.form.get('ssl', 'false') == 'true'
        refresh_interval = request.form.get('refresh_interval', '5').strip()

        rules: Optional[List[Tuple[bool, Dict]]] = json.loads(request.form.get('rules', '').strip())
        
        # 输入验证
        errors = []
        if not apikey:
            errors.append("API Key 不能为空。")
        if not host:
            errors.append("Host 不能为空。")
        if not port.isdigit():
            errors.append("Port 必须是数字。")
        if not refresh_interval.isdigit():
            errors.append("Refresh Interval 必须是数字。")

        if errors:
            message = " ".join(errors)
            category = "error"
        else:
            # 更新配置
            new_config_data = {
                "apikey": apikey,
                "host": host,
                "port": int(port),
                "ssl": ssl,
                "rules": rules,
                "refresh_interval": int(refresh_interval)
            }

            utils.config.update_config(new_config_data)
            message = "配置已成功更新！"
            category = "success"

    apikey = utils.config.config.apikey
    host = utils.config.config.host
    port = utils.config.config.port
    ssl = utils.config.config.ssl
    rules = utils.config.config.rules
    refresh_interval = utils.config.config.refresh_interval

    texts = {
        'title': 'Sonarr 自动删除慢速下载',
        'submit': '提交',
    
        # Confirmations and Alerts
        'delete_warning': '确定要删除这条规则吗？',
    
        # Rules Management
        'add_rule': '添加新规则',
        'edit': '编辑',
        'delete': '删除',
    
        # Rule Details
        'downloaded_time': '已下载时间',
        'status': '状态',
        'avg_speed': '平均下载速度',
        'estimated_time': '预计剩余时间',
        'progress': '下载进度',
    
        # Rule Field Labels (used in the modal)
        'downloaded_time_label': 'C1: 下载时间超过以下分钟',
        'status_label': 'C2: 当状态包含以下（用逗号分隔）',
        'avg_speed_label': 'C3: 平均下载速度低于以下值（kb/s）',
        'estimated_time_label': 'C4: 预计下载时间超过以下值（分钟）',
        'progress_label': 'C5: 下载百分比小于以下值(0～100)',
    
        # Modal
        'edit_rule_modal_title': '编辑规则',
        'save_button': '保存',
        'cancel_button': '取消'
    }


    template = """
    <html>

<head>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f0f2f5;
        }

        .form-container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            max-width: 800px;
            margin: auto;
        }

        h1 {
            text-align: center;
            color: #333;
        }

        label {
            display: block;
            margin-top: 10px;
            font-weight: bold;
        }

        .required {
            color: red;
        }

        input[type="text"],
        input[type="number"],
        input[type="submit"] {
            width: 100%;
            padding: 8px;
            margin-top: 5px;
            box-sizing: border-box;
        }

        input[type="submit"] {
            padding: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            margin-top: 20px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        input[type="submit"]:hover {
            background-color: #0056b3;
        }

        .message {
            text-align: center;
            margin-top: 20px;
            padding: 10px;
            border-radius: 5px;
            color: #fff;
            opacity: 0;
            animation: fadeIn 1s forwards, slideIn 1s forwards;
        }

        .error {
            background-color: #f8d7da;
            color: #721c24;
        }

        .success {
            background-color: #d4edda;
            color: #155724;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
            }

            to {
                opacity: 1;
            }
        }

        @keyframes slideIn {
            from {
                transform: translateY(-20px);
            }

            to {
                transform: translateY(0);
            }
        }

        .rule-box {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
            transition: all 0.3s ease;
        }

        .rule-box:hover {
            box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
        }

        .rule-controls {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
        }

        .rule-left,
        .rule-right {
            display: flex;
            align-items: center;
        }

        .rule-actions {
            gap: 10px;
        }

        .edit-btn,
        .delete-btn {
            padding: 2px 8px;
            border: none;
            border-radius: 3px;
            cursor: pointer;
        }

        .edit-btn {
            background-color: #4CAF50;
            color: white;
        }

        .delete-btn {
            background-color: #f44336;
            color: white;
        }

        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 1000;
        }

        .modal-content {
            background-color: #fff;
            margin: 15% auto;
            padding: 20px;
            border-radius: 5px;
            width: 80%;
            max-width: 500px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        .form-group {
            margin-bottom: 15px;
        }

        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
        }

        .form-control {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }

        .modal-footer {
            margin-top: 20px;
            text-align: right;
        }

        .btn {
            padding: 8px 16px;
            border-radius: 4px;
            border: none;
            cursor: pointer;
            margin-left: 10px;
        }

        .btn-primary {
            background-color: #007bff;
            color: white;
        }

        .btn-primary:hover {
            background-color: #0056b3;
        }

        .btn-secondary {
            background-color: #6c757d;
            color: white;
        }

        .btn-secondary:hover {
            background-color: #545b62;
        }

        h3 {
            margin-top: 0;
            margin-bottom: 20px;
            color: #333;
        }
    </style>

<script>
    // 初始化数据
    const rules = {{ rules | tojson | safe }} || [];
    const texts = {{ texts | tojson | safe }};
    let currentEditIndex = -1;

    // 常量定义
    const RULE_FIELDS = ['C1', 'C2', 'C3', 'C4', 'C5'];
    const FIELD_LABELS = {
        'C1': 'downloaded_time',
        'C2': 'status',
        'C3': 'avg_speed',
        'C4': 'estimated_time',
        'C5': 'progress'
    };
    const FIELD_UNITS = {
        'C1': 'min',
        'C2': '',
        'C3': 'kb/s',
        'C4': 'min',
        'C5': '%'
    };

    // 工具函数
    function getElementValue(id) {
        return document.getElementById(id).value || null;
    }

    function createRuleObject() {
        const ruleObj = {};
        RULE_FIELDS.forEach(field => {
            const value = getElementValue(field);
            if (value !== null) {
                ruleObj[field] = value;
            }
        });
        return ruleObj;
    }

    function renderRuleContent(rule) {
        let content = '';
        Object.entries(rule).forEach(([key, value]) => {
            if (value !== null && FIELD_LABELS[key]) {
                content += `<div>${texts[FIELD_LABELS[key]]}: ${value}${FIELD_UNITS[key]}</div>`;
            }
        });
        return content;
    }

    // 主要功能函数
    function updateRulesInput() {
        try {
            const rules_input = JSON.parse(document.getElementById("rulesInput").value);
            const updatedRule = createRuleObject();

            if (currentEditIndex !== -1) {
                updateExistingRule(rules_input, updatedRule);
            } else {
                createNewRule(rules_input, updatedRule);
            }

            document.getElementById("rulesInput").value = JSON.stringify(rules_input);
        } catch (error) {
            console.error('Error updating rules:', error);
            alert('更新规则时发生错误');
        }
    }

    function updateExistingRule(rules_input, updatedRule) {
        const ruleBox = document.querySelector(`.rules-container .rule-box[data-index="${currentEditIndex}"]`);
        if (ruleBox) {
            const ruleContent = ruleBox.querySelector(".rule-content");
            ruleContent.innerHTML = renderRuleContent(updatedRule);
            rules_input[currentEditIndex][1] = updatedRule;
        }
    }
    
    function refreshRulesDisplay(rules_input) {
        const rulesContainer = document.querySelector('.rules-container');
        
        // 清除所有现有规则（保留添加按钮）
        const addRuleBox = rulesContainer.querySelector('.rule-box:last-child');
        rulesContainer.innerHTML = '';
        rulesContainer.appendChild(addRuleBox);
        
        // 重新渲染每个规则
        rules_input.forEach((rule, index) => {
            const ruleBox = document.createElement('div');
            ruleBox.classList.add('rule-box');
            ruleBox.setAttribute('data-index', index);
            
            ruleBox.innerHTML = `
                <div class="rule-controls">
                    <div class="rule-left">
                        <input type="checkbox" class="rule-checkbox" ${rule[0] ? 'checked' : ''}>
                    </div>
                    <div class="rule-right">
                        <div class="edit-btn" onclick="editRule(${index})">${texts['edit']}</div>
                        <div class="delete-btn" onclick="deleteRule(${index})">${texts['delete']}</div>
                    </div>
                </div>
                <div class="rule-content">
                    ${renderRuleContent(rule[1])}
                </div>
            `;
            
            rulesContainer.insertBefore(ruleBox, addRuleBox);
        });
    }

    function createNewRule(rules_input, updatedRule) {
        const rulesContainer = document.querySelector('.rules-container');
        const newRuleBox = document.createElement('div');
        newRuleBox.classList.add('rule-box');
        newRuleBox.setAttribute('data-index', 'new');

        newRuleBox.innerHTML = `
            <div class="rule-controls">
                <div class="rule-left">
                    <input type="checkbox" class="rule-checkbox" checked>
                </div>
                <div class="rule-right">
                    <div class="edit-btn" onclick="editRule('new')">编辑</div>
                    <div class="delete-btn" onclick="deleteRule('new')">删除</div>
                </div>
            </div>
            <div class="rule-content">${renderRuleContent(updatedRule)}</div>
        `;

        rulesContainer.appendChild(newRuleBox);
        rules_input.push([true, updatedRule]);
    }

    function editRule(index) {
        currentEditIndex = index;
        const rule = rules[index][1];

        RULE_FIELDS.forEach(key => {
            document.getElementById(key).value = rule[key] || '';
        });

        document.getElementById('ruleModal').style.display = 'block';
    }

    function addRule() {
        currentEditIndex = -1;
        RULE_FIELDS.forEach(key => {
            document.getElementById(key).value = '';
        });
        document.getElementById('ruleModal').style.display = 'block';
    }

    function saveRule() {
        const ruleData = createRuleObject();

        if (currentEditIndex === -1) {
            rules.push([true, ruleData]);
        } else {
            rules[currentEditIndex][1] = ruleData;
        }
        
        updateRulesInput();
        closeModal();
    }

    function deleteRule(index) {
        if (confirm(texts['delete_warning'])) {

        const rules_input = JSON.parse(document.getElementById("rulesInput").value);
        rules_input.splice(index, 1);

        document.getElementById("rulesInput").value = JSON.stringify(rules_input);

        refreshRulesDisplay(rules_input);
    }
    }

    function closeModal() {
        document.getElementById('ruleModal').style.display = 'none';
    }
</script>
</head>

<body>
    <div class="form-container">
        <h1>{{ texts['title'] }}</h1>
        {% if message %}
        <div class="message {{ category }}">{{ message }}</div>
        {% endif %}
        <form method="post">
            <label>API Key <span class="required">*</span>:</label>
            <input type="text" name="apikey" value="{{ apikey }}"><br>
            <label>Host <span class="required">*</span>:</label>
            <input type="text" name="host" value="{{ host }}"><br>
            <label>Port:</label>
            <input type="text" name="port" value="{{ port }}"><br>
            <label>SSL:</label>
            <input type="checkbox" name="ssl" value="true" {% if ssl %}checked{% endif %}><br>
            <label>Refresh Interval:</label>
            <input type="text" name="refresh_interval" value="{{ refresh_interval }}"><br>

            <div class="rules-container">
                {% for rule in rules %}
                <div class="rule-box" data-index="{{ loop.index0 }}">
                    <div class="rule-controls">
                        <div class="rule-left">
                            <input type="checkbox" class="rule-checkbox" {% if rule[1].get('enabled', True) %}checked{% endif %}>
                        </div>
                        <div class="rule-right">
                            <div class="edit-btn" onclick="editRule({{ loop.index0 }})">{{ texts['edit'] }}</div>
                            <div class="delete-btn" onclick="deleteRule({{ loop.index0 }})">{{ texts['delete'] }}</div>
                        </div>
                    </div>
                    <div class="rule-content">
                        {% for key, value in rule[1].items() %}
                        <div>
                            {% if key == 'C1' %}
                            {{ texts['downloaded_time'] }}: {{ value }}分钟
                            {% elif key == 'C2' %}
                            {{ texts['status'] }}: {{ value }}
                            {% elif key == 'C3' %}
                            {{ texts['avg_speed'] }}: {{ value }}kb/s
                            {% elif key == 'C4' %}
                            {{ texts['estimated_time'] }}: {{ value }}分钟
                            {% elif key == 'C5' %}
                            {{ texts['progress'] }}: {{ value }}%
                            {% endif %}
                        </div>
                        {% endfor %}
                    </div>
                </div>
                {% endfor %}
                
                <div class="rule-box">
                    <div class="rule-btn" onclick="addRule()">{{ texts['add_rule'] }}</div>
                </div>
            </div>

            <input type="hidden" name="rules" id="rulesInput" value='{{ rules | tojson }}'>
            <input type="submit" value="{{ texts['submit'] }}">
        </form>
    </div>

    <!-- Modal for Editing Rule -->
    <div id="ruleModal" class="modal">
        <div class="modal-content">
            <h3>{{ texts['edit_rule_modal_title'] }}</h3>

            <div class="form-group">
                <label>{{ texts['downloaded_time_label'] }}</label>
                <input type="number" id="C1" min="0" class="form-control">
            </div>

            <div class="form-group">
                <label>{{ texts['status_label'] }}</label>
                <input type="text" id="C2" class="form-control">
            </div>

            <div class="form-group">
                <label>{{ texts['avg_speed_label'] }}</label>
                <input type="number" id="C3" min="0" class="form-control">
            </div>

            <div class="form-group">
                <label>{{ texts['estimated_time_label'] }}</label>
                <input type="number" id="C4" min="0" class="form-control">
            </div>

            <div class="form-group">
                <label>{{ texts['progress_label'] }}</label>
                <input type="number" id="C5" min="0" max="100" class="form-control">
            </div>

            <div class="modal-footer">
                <button class="btn btn-secondary" onclick="closeModal()">{{ texts['cancel_button'] }}</button>
                <button class="btn btn-primary" onclick="saveRule()">{{ texts['save_button'] }}</button>
            </div>
        </div>
    </div>

</body>

</html>
    """

    return render_template_string(
        template,
        apikey=apikey,
        host=host,
        port=port,
        ssl=ssl,
        rules=rules,
        refresh_interval=refresh_interval,
        message=message,
        category=category,
        texts=texts
    )
