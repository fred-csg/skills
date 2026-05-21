import os
import re
import json

def parse_markdown(filepath):
    categories = []
    current_category = None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        line_str = line.strip()
        
        # Match category header
        # E.g., ## <a name="academic"></a>📂 Pesquisa e Escrita Acadêmica
        cat_match = re.match(r'^##\s*<a\s+name="([^"]+)"></a>📂\s*(.*)', line_str)
        if cat_match:
            slug = cat_match.group(1)
            title = cat_match.group(2).strip()
            current_category = {
                'slug': slug,
                'title': title,
                'description': '',
                'skills': []
            }
            categories.append(current_category)
            continue
            
        # Match description (italic line under the category header)
        if current_category and not current_category['description'] and line_str.startswith('*') and line_str.endswith('*'):
            current_category['description'] = line_str.strip('*')
            continue
            
        # Match table rows
        if current_category and line_str.startswith('|'):
            if 'Habilidade' in line_str or '---' in line_str:
                continue
            
            # This is a skill row
            parts = [p.strip() for p in line_str.split('|')[1:-1]]
            if len(parts) >= 3:
                skill_name_raw = parts[0]
                desc = parts[1]
                link_raw = parts[2]
                
                # Extract clean skill name from **Skill Name**
                name_match = re.match(r'^\*\*([^*]+)\*\*$', skill_name_raw)
                skill_name = name_match.group(1) if name_match else skill_name_raw
                
                # Extract link title and URL
                # E.g., [SKILL.md](file:///g:/SKILLS/academic/academic-paper-summarizer/SKILL.md)
                link_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', link_raw)
                link_title = link_match.group(1) if link_match else 'Link'
                link_url = link_match.group(2) if link_match else ''
                
                # Clean up local path for displaying/copying
                local_path = link_url.replace('file:///', '').replace('/', '\\')
                
                current_category['skills'].append({
                    'name': skill_name,
                    'description': desc,
                    'link_url': link_url,
                    'local_path': local_path
                })
                
    return categories

def generate_html(categories, output_path):
    # Total count calculation
    total_skills = sum(len(c['skills']) for c in categories)
    total_categories = len(categories)
    
    # JSON dump for embedding
    categories_json = json.dumps(categories, ensure_ascii=False, indent=2)
    
    # Using raw string (r""") to preserve all backslashes exactly as they are for CSS/JS
    html_template = r"""<!DOCTYPE html>
<html lang="pt-BR" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catálogo de Skills - Antigravity</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>

    <style>
        :root {
            /* Dark Theme Variables */
            --bg-body: #090d16;
            --bg-grid-color: rgba(99, 102, 241, 0.03);
            --card-bg: rgba(17, 24, 39, 0.6);
            --card-border: rgba(255, 255, 255, 0.05);
            --card-hover-border: rgba(99, 102, 241, 0.4);
            --card-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            --sidebar-bg: rgba(13, 18, 30, 0.85);
            --sidebar-border: rgba(255, 255, 255, 0.05);
            --header-bg: rgba(9, 13, 22, 0.8);
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --text-muted: #6b7280;
            --accent-color: #6366f1;
            --accent-secondary: #06b6d4;
            --accent-gradient: linear-gradient(135deg, #6366f1, #06b6d4);
            --glow-color: rgba(99, 102, 241, 0.15);
            --input-bg: rgba(17, 24, 39, 0.8);
            --input-border: rgba(255, 255, 255, 0.08);
            --tag-bg: rgba(99, 102, 241, 0.1);
            --tag-text: #818cf8;
            --mark-bg: rgba(234, 179, 8, 0.3);
            --mark-text: #fef08a;
            --table-row-hover: rgba(31, 41, 55, 0.4);
            --scrollbar-thumb: rgba(255, 255, 255, 0.1);
            --scrollbar-thumb-hover: rgba(255, 255, 255, 0.2);
        }

        [data-theme="light"] {
            /* Light Theme Variables */
            --bg-body: #f8fafc;
            --bg-grid-color: rgba(79, 70, 229, 0.02);
            --card-bg: rgba(255, 255, 255, 0.8);
            --card-border: rgba(0, 0, 0, 0.06);
            --card-hover-border: rgba(79, 70, 229, 0.4);
            --card-shadow: 0 10px 30px -10px rgba(148, 163, 184, 0.15);
            --sidebar-bg: rgba(248, 250, 252, 0.9);
            --sidebar-border: rgba(0, 0, 0, 0.06);
            --header-bg: rgba(248, 250, 252, 0.8);
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --text-muted: #64748b;
            --accent-color: #4f46e5;
            --accent-secondary: #0891b2;
            --accent-gradient: linear-gradient(135deg, #4f46e5, #0891b2);
            --glow-color: rgba(79, 70, 229, 0.05);
            --input-bg: #ffffff;
            --input-border: rgba(0, 0, 0, 0.1);
            --tag-bg: rgba(79, 70, 229, 0.08);
            --tag-text: #4f46e5;
            --mark-bg: rgba(250, 204, 21, 0.4);
            --mark-text: #713f12;
            --table-row-hover: rgba(241, 245, 249, 0.8);
            --scrollbar-thumb: rgba(0, 0, 0, 0.1);
            --scrollbar-thumb-hover: rgba(0, 0, 0, 0.2);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            transition: background-color 0.3s ease, border-color 0.3s ease;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-body);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
            background-image: radial-gradient(var(--bg-grid-color) 1px, transparent 1px);
            background-size: 24px 24px;
        }

        /* Scrollbar Styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        ::-webkit-scrollbar-thumb {
            background: var(--scrollbar-thumb);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--scrollbar-thumb-hover);
        }

        /* Layout Structure */
        .app-container {
            display: flex;
            flex: 1;
            position: relative;
        }

        /* Sidebar Styling */
        aside {
            width: 320px;
            background-color: var(--sidebar-bg);
            border-right: 1px solid var(--sidebar-border);
            backdrop-filter: blur(20px);
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            position: sticky;
            top: 0;
            height: 100vh;
            overflow-y: auto;
            z-index: 10;
        }

        .brand-section {
            display: flex;
            align-items: center;
            gap: 12px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--sidebar-border);
        }

        .brand-logo {
            background: var(--accent-gradient);
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            box-shadow: 0 0 20px var(--glow-color);
        }

        .brand-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.25rem;
            font-weight: 700;
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .sidebar-title {
            font-family: 'Outfit', sans-serif;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            margin-bottom: 10px;
        }

        .category-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .category-item {
            padding: 10px 12px;
            border-radius: 8px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: space-between;
            color: var(--text-secondary);
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            user-select: none;
        }

        .category-item:hover {
            background-color: rgba(99, 102, 241, 0.08);
            color: var(--text-primary);
        }

        .category-item.active {
            background: var(--accent-gradient);
            color: white;
            box-shadow: 0 4px 15px var(--glow-color);
        }

        .category-count {
            background-color: var(--input-border);
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .category-item.active .category-count {
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
        }

        /* Main Content Styling */
        main {
            flex: 1;
            padding: 40px;
            display: flex;
            flex-direction: column;
            gap: 30px;
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
        }

        /* Sticky Header */
        header {
            display: flex;
            flex-direction: column;
            gap: 20px;
            background-color: var(--header-bg);
            backdrop-filter: blur(10px);
            padding: 20px 0;
            position: sticky;
            top: 0;
            z-index: 9;
            border-bottom: 1px solid var(--sidebar-border);
        }

        .header-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
        }

        .stats-summary {
            display: flex;
            gap: 24px;
        }

        .stat-card {
            display: flex;
            flex-direction: column;
        }

        .stat-val {
            font-family: 'Outfit', sans-serif;
            font-size: 2.2rem;
            font-weight: 800;
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1.1;
        }

        .stat-label {
            font-size: 0.8rem;
            color: var(--text-secondary);
            font-weight: 500;
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        /* Control Button Styles */
        .btn-control {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            color: var(--text-secondary);
            width: 44px;
            height: 44px;
            border-radius: 10px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
        }

        .btn-control:hover {
            border-color: var(--accent-color);
            color: var(--text-primary);
            box-shadow: 0 0 10px var(--glow-color);
            transform: translateY(-2px);
        }

        /* Search Section */
        .search-container {
            position: relative;
            flex: 1;
            max-width: 600px;
        }

        .search-icon {
            position: absolute;
            left: 16px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            pointer-events: none;
            width: 18px;
            height: 18px;
        }

        .search-input {
            width: 100%;
            background-color: var(--input-bg);
            border: 1px solid var(--input-border);
            border-radius: 12px;
            padding: 14px 16px 14px 48px;
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem;
            outline: none;
            transition: all 0.2s;
        }

        .search-input:focus {
            border-color: var(--accent-color);
            box-shadow: 0 0 15px var(--glow-color);
        }

        /* Section Category Header */
        .section-header {
            padding-bottom: 12px;
            border-bottom: 2px solid var(--card-border);
            margin-top: 10px;
            scroll-margin-top: 150px;
        }

        .section-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.6rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
            color: var(--text-primary);
        }

        .section-desc {
            font-size: 0.95rem;
            color: var(--text-secondary);
            margin-top: 6px;
            font-style: italic;
        }

        /* Grid View Layout */
        .skills-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }

        .skill-card {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            box-shadow: var(--card-shadow);
            backdrop-filter: blur(12px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            animation: fadeIn 0.4s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .skill-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: var(--accent-gradient);
            opacity: 0;
            transition: opacity 0.3s;
        }

        .skill-card:hover {
            transform: translateY(-5px);
            border-color: var(--card-hover-border);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2), 0 0 15px var(--glow-color);
        }

        .skill-card:hover::before {
            opacity: 1;
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 10px;
        }

        .skill-name {
            font-family: 'Outfit', sans-serif;
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--text-primary);
        }

        .skill-desc {
            font-size: 0.9rem;
            line-height: 1.5;
            color: var(--text-secondary);
            flex: 1;
        }

        .skill-path-container {
            background-color: rgba(0, 0, 0, 0.15);
            padding: 8px 12px;
            border-radius: 8px;
            border: 1px solid var(--card-border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
        }

        .skill-path {
            font-family: 'Fira Code', monospace;
            font-size: 0.75rem;
            color: var(--text-muted);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .card-actions {
            display: flex;
            gap: 10px;
        }

        .btn-action {
            flex: 1;
            padding: 10px 12px;
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            transition: all 0.2s;
            border: 1px solid var(--card-border);
            background-color: rgba(255, 255, 255, 0.03);
            color: var(--text-secondary);
            text-decoration: none;
        }

        .btn-action:hover {
            background-color: var(--accent-color);
            color: white;
            border-color: var(--accent-color);
            box-shadow: 0 4px 12px var(--glow-color);
        }

        .btn-action-primary {
            background: var(--accent-gradient);
            color: white;
            border: none;
        }

        .btn-action-primary:hover {
            opacity: 0.9;
            transform: translateY(-1px);
        }

        /* Table View Layout */
        .table-container {
            width: 100%;
            overflow-x: auto;
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            box-shadow: var(--card-shadow);
            margin-bottom: 40px;
            display: none;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.9rem;
        }

        th {
            background-color: rgba(0, 0, 0, 0.1);
            color: var(--text-secondary);
            font-weight: 600;
            padding: 16px 20px;
            border-bottom: 1px solid var(--card-border);
            font-family: 'Outfit', sans-serif;
        }

        td {
            padding: 16px 20px;
            border-bottom: 1px solid var(--card-border);
            color: var(--text-primary);
            vertical-align: middle;
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr:hover td {
            background-color: var(--table-row-hover);
        }

        .table-skill-name {
            font-weight: 600;
            color: var(--text-primary);
        }

        .table-skill-path {
            font-family: 'Fira Code', monospace;
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        .table-actions {
            display: flex;
            gap: 8px;
        }

        .btn-table-action {
            width: 32px;
            height: 32px;
            border-radius: 6px;
            border: 1px solid var(--card-border);
            background-color: rgba(255, 255, 255, 0.02);
            color: var(--text-secondary);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
            text-decoration: none;
        }

        .btn-table-action:hover {
            background-color: var(--accent-color);
            color: white;
            border-color: var(--accent-color);
        }

        /* Highlights */
        mark {
            background-color: var(--mark-bg);
            color: var(--mark-text);
            border-radius: 2px;
            padding: 0 2px;
        }

        /* Empty State */
        .empty-state {
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 16px;
            padding: 60px 20px;
            text-align: center;
            color: var(--text-secondary);
        }

        .empty-state-icon {
            width: 48px;
            height: 48px;
            color: var(--text-muted);
        }

        /* Toast Feedback */
        .toast {
            position: fixed;
            bottom: 24px;
            right: 24px;
            background-color: #10b981;
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.9rem;
            box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);
            display: flex;
            align-items: center;
            gap: 8px;
            transform: translateY(100px);
            opacity: 0;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            z-index: 999;
        }

        .toast.show {
            transform: translateY(0);
            opacity: 1;
        }

        /* Category Grid Container */
        .category-block {
            margin-bottom: 20px;
        }

        /* Collapsible sidebar on mobile */
        @media (max-width: 900px) {
            .app-container {
                flex-direction: column;
            }
            aside {
                width: 100%;
                height: auto;
                position: relative;
                border-right: none;
                border-bottom: 1px solid var(--sidebar-border);
            }
            main {
                padding: 20px;
            }
        }
    </style>
</head>
<body>

    <div class="app-container">
        <!-- Sidebar -->
        <aside>
            <div class="brand-section">
                <div class="brand-logo">
                    <i data-lucide="zap"></i>
                </div>
                <div class="brand-title">Antigravity</div>
            </div>
            
            <div>
                <h3 class="sidebar-title">Categorias</h3>
                <ul class="category-list" id="categoryList">
                    <li class="category-item active" data-slug="all" onclick="selectCategory('all')">
                        <span>Mostrar Todas</span>
                        <span class="category-count" id="totalCountBadge">{{TOTAL_SKILLS}}</span>
                    </li>
                    <!-- Dynamic Categories Inserted Here -->
                </ul>
            </div>
        </aside>

        <!-- Main Content -->
        <main>
            <header>
                <div class="header-top">
                    <div class="stats-summary">
                        <div class="stat-card">
                            <span class="stat-val" id="skillsCount">{{TOTAL_SKILLS}}</span>
                            <span class="stat-label">Habilidades</span>
                        </div>
                        <div class="stat-card">
                            <span class="stat-val">{{TOTAL_CATEGORIES}}</span>
                            <span class="stat-label">Categorias</span>
                        </div>
                    </div>

                    <div class="header-actions">
                        <!-- Theme Toggle -->
                        <button class="btn-control" id="themeToggle" onclick="toggleTheme()" title="Alternar Tema">
                            <i data-lucide="sun" id="themeIcon"></i>
                        </button>
                        <!-- Layout Toggle -->
                        <button class="btn-control" id="layoutToggle" onclick="toggleLayout()" title="Alternar Visualização">
                            <i data-lucide="layout-grid" id="layoutIcon"></i>
                        </button>
                    </div>
                </div>

                <div class="search-container">
                    <i data-lucide="search" class="search-icon"></i>
                    <input type="text" id="searchInput" class="search-input" placeholder="Pesquise por habilidades, termos, caminhos..." oninput="handleSearch()">
                </div>
            </header>

            <!-- Skills Containers -->
            <div id="skillsViewContainer">
                <!-- Grid View -->
                <div id="skillsGrid" class="skills-grid">
                    <!-- Dynamic Cards -->
                </div>

                <!-- Table View -->
                <div id="skillsTableContainer" class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Habilidade</th>
                                <th>Categoria</th>
                                <th>Descrição</th>
                                <th>Caminho</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody id="skillsTableBody">
                            <!-- Dynamic Rows -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Empty State -->
            <div class="empty-state" id="emptyState">
                <i data-lucide="search-code" class="empty-state-icon"></i>
                <h2>Nenhuma habilidade encontrada</h2>
                <p>Tente refinar sua busca ou escolher outra categoria.</p>
            </div>
        </main>
    </div>

    <!-- Toast Notification -->
    <div id="toast" class="toast">
        <i data-lucide="check-circle-2"></i>
        <span id="toastText">Copiado com sucesso!</span>
    </div>

    <script>
        // Data Payload injected from Python compiler
        const categoriesData = {{CATEGORIES_JSON}};
        
        // App State
        let currentCategory = 'all';
        let searchQuery = '';
        let currentLayout = 'grid'; // grid or table

        // Initialize Icons
        lucide.createIcons();

        // Render Categories list in Sidebar
        function renderCategorySidebar() {
            const listContainer = document.getElementById('categoryList');
            
            // Clear dynamic elements (keep the first item "Show All")
            while (listContainer.children.length > 1) {
                listContainer.removeChild(listContainer.lastChild);
            }

            categoriesData.forEach(cat => {
                if (cat.skills.length === 0) return;
                
                const li = document.createElement('li');
                li.className = 'category-item';
                li.setAttribute('data-slug', cat.slug);
                li.onclick = () => selectCategory(cat.slug);
                
                li.innerHTML = `
                    <span>📂 ${cat.title}</span>
                    <span class="category-count">${cat.skills.length}</span>
                `;
                listContainer.appendChild(li);
            });
        }

        // Handle Category Selection
        function selectCategory(slug) {
            currentCategory = slug;
            
            // Update Active Class in Sidebar
            const items = document.querySelectorAll('.category-item');
            items.forEach(item => {
                if (item.getAttribute('data-slug') === slug) {
                    item.classList.add('active');
                } else {
                    item.classList.remove('active');
                }
            });

            renderActiveView();
        }

        // Handle Search Inputs
        function handleSearch() {
            searchQuery = document.getElementById('searchInput').value.trim().toLowerCase();
            renderActiveView();
        }

        // Helper to Highlight Matching Query
        function highlightMatch(text, query) {
            if (!query) return text;
            const index = text.toLowerCase().indexOf(query);
            if (index === -1) return text;
            
            // Regex match to make it case-insensitive highlight
            const regex = new RegExp(`(${escapeRegExp(query)})`, 'gi');
            return text.replace(regex, '<mark>$1</mark>');
        }

        function escapeRegExp(string) {
            return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        }

        // Filter and collect skills based on state
        function getFilteredSkills() {
            let skillsList = [];
            
            categoriesData.forEach(cat => {
                if (currentCategory === 'all' || currentCategory === cat.slug) {
                    cat.skills.forEach(skill => {
                        const nameMatch = skill.name.toLowerCase().includes(searchQuery);
                        const descMatch = skill.description.toLowerCase().includes(searchQuery);
                        const pathMatch = skill.local_path.toLowerCase().includes(searchQuery);
                        const catMatch = cat.title.toLowerCase().includes(searchQuery);
                        
                        if (nameMatch || descMatch || pathMatch || catMatch) {
                            skillsList.push({
                                ...skill,
                                categoryTitle: cat.title,
                                categorySlug: cat.slug
                            });
                        }
                    });
                }
            });

            return skillsList;
        }

        // Render functions
        function renderActiveView() {
            const filteredSkills = getFilteredSkills();
            
            // Update Counter
            document.getElementById('skillsCount').innerText = filteredSkills.length;
            
            // Toggle Empty State
            const emptyState = document.getElementById('emptyState');
            const skillsGrid = document.getElementById('skillsGrid');
            const skillsTableContainer = document.getElementById('skillsTableContainer');

            if (filteredSkills.length === 0) {
                emptyState.style.display = 'flex';
                skillsGrid.style.display = 'none';
                skillsTableContainer.style.display = 'none';
                return;
            } else {
                emptyState.style.display = 'none';
            }

            if (currentLayout === 'grid') {
                skillsGrid.style.display = 'grid';
                skillsTableContainer.style.display = 'none';
                renderGridView(filteredSkills);
            } else {
                skillsGrid.style.display = 'none';
                skillsTableContainer.style.display = 'block';
                renderTableView(filteredSkills);
            }
            
            lucide.createIcons();
        }

        function renderGridView(skills) {
            const gridContainer = document.getElementById('skillsGrid');
            gridContainer.innerHTML = '';

            skills.forEach(skill => {
                const card = document.createElement('div');
                card.className = 'skill-card';
                
                const highlightedName = highlightMatch(skill.name, searchQuery);
                const highlightedDesc = highlightMatch(skill.description, searchQuery);
                const highlightedPath = highlightMatch(skill.local_path, searchQuery);
                
                card.innerHTML = `
                    <div class="card-header">
                        <span class="skill-name">${highlightedName}</span>
                        <span style="font-size:0.75rem; font-weight:600; padding:4px 8px; border-radius:6px; background-color:var(--tag-bg); color:var(--tag-text);">
                            ${skill.categoryTitle}
                        </span>
                    </div>
                    <p class="skill-desc">${highlightedDesc}</p>
                    <div class="skill-path-container">
                        <span class="skill-path" title="${skill.local_path}">${highlightedPath}</span>
                        <button onclick="copyToClipboard('${escapeJsString(skill.local_path)}', 'Caminho copiado!')" style="background:none; border:none; cursor:pointer; color:var(--text-muted); display:flex; align-items:center;" title="Copiar Caminho">
                            <i data-lucide="copy" style="width:14px; height:14px;"></i>
                        </button>
                    </div>
                    <div class="card-actions">
                        <a href="${skill.link_url}" class="btn-action btn-action-primary" target="_blank">
                            <i data-lucide="external-link" style="width:14px; height:14px;"></i> Abrir
                        </a>
                        <button class="btn-action" onclick="copyMarkdownLink('${escapeJsString(skill.name)}', '${escapeJsString(skill.link_url)}')">
                            <i data-lucide="link" style="width:14px; height:14px;"></i> MD Link
                        </button>
                    </div>
                `;
                gridContainer.appendChild(card);
            });
        }

        function renderTableView(skills) {
            const tbody = document.getElementById('skillsTableBody');
            tbody.innerHTML = '';

            skills.forEach(skill => {
                const tr = document.createElement('tr');
                
                const highlightedName = highlightMatch(skill.name, searchQuery);
                const highlightedDesc = highlightMatch(skill.description, searchQuery);
                const highlightedPath = highlightMatch(skill.local_path, searchQuery);

                tr.innerHTML = `
                    <td class="table-skill-name">${highlightedName}</td>
                    <td><span style="font-size:0.75rem; font-weight:600; padding:4px 8px; border-radius:6px; background-color:var(--tag-bg); color:var(--tag-text); whitespace:nowrap;">${skill.categoryTitle}</span></td>
                    <td class="skill-desc">${highlightedDesc}</td>
                    <td class="table-skill-path" title="${skill.local_path}">${highlightedPath}</td>
                    <td>
                        <div class="table-actions">
                            <a href="${skill.link_url}" class="btn-table-action" target="_blank" title="Abrir Habilidade">
                                <i data-lucide="external-link" style="width:14px; height:14px;"></i>
                            </a>
                            <button class="btn-table-action" onclick="copyMarkdownLink('${escapeJsString(skill.name)}', '${escapeJsString(skill.link_url)}')" title="Copiar Markdown Link">
                                <i data-lucide="link" style="width:14px; height:14px;"></i>
                            </button>
                            <button class="btn-table-action" onclick="copyToClipboard('${escapeJsString(skill.local_path)}', 'Caminho copiado!')" title="Copiar Caminho Local">
                                <i data-lucide="copy" style="width:14px; height:14px;"></i>
                            </button>
                        </div>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        // Layout Switcher
        function toggleLayout() {
            currentLayout = currentLayout === 'grid' ? 'table' : 'grid';
            const icon = document.getElementById('layoutIcon');
            
            if (currentLayout === 'grid') {
                icon.setAttribute('data-lucide', 'layout-grid');
            } else {
                icon.setAttribute('data-lucide', 'list');
            }
            
            renderActiveView();
        }

        // Theme Switcher
        function toggleTheme() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('skills-theme', newTheme);
            
            const themeIcon = document.getElementById('themeIcon');
            themeIcon.setAttribute('data-lucide', newTheme === 'dark' ? 'sun' : 'moon');
            lucide.createIcons();
        }

        // Init Theme from LocalStorage
        const savedTheme = localStorage.getItem('skills-theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
        document.getElementById('themeIcon').setAttribute('data-lucide', savedTheme === 'dark' ? 'sun' : 'moon');

        // Copy Clipboard Helpers
        function copyToClipboard(text, successMessage) {
            navigator.clipboard.writeText(text).then(() => {
                showToast(successMessage);
            }).catch(err => {
                console.error('Failed to copy: ', err);
            });
        }

        // Generate markdown link with file:/// protocol
        function copyMarkdownLink(name, url) {
            const md = `[${name}](${url})`;
            copyToClipboard(md, 'Link Markdown copiado!');
        }

        // Helper to safely escape characters inside inline JavaScript strings
        function escapeJsString(str) {
            return str
                .replace(/\\/g, '\\\\')
                .replace(/'/g, "\\'")
                .replace(/"/g, '\\"')
                .replace(/\n/g, '\\n')
                .replace(/\r/g, '\\r');
        }

        function showToast(message) {
            const toast = document.getElementById('toast');
            document.getElementById('toastText').innerText = message;
            toast.classList.add('show');
            setTimeout(() => {
                toast.classList.remove('show');
            }, 2000);
        }

        // Init Execution
        renderCategorySidebar();
        renderActiveView();
    </script>
</body>
</html>
"""

    # Do the actual replacements
    html_template = html_template.replace("{{CATEGORIES_JSON}}", categories_json)
    html_template = html_template.replace("{{TOTAL_SKILLS}}", str(total_skills))
    html_template = html_template.replace("{{TOTAL_CATEGORIES}}", str(total_categories))

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"Index HTML generated at: {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    md_file = os.path.join(base_dir, "indice-skills.md")
    html_file = os.path.join(base_dir, "indice-skills.html")
    
    if os.path.exists(md_file):
        categories = parse_markdown(md_file)
        generate_html(categories, html_file)
    else:
        print(f"Error: {md_file} not found.")
