# Dev.Rodrigo — portfólio

Site pessoal de Rodrigo Guimarães. HTML e CSS puros, sem build e sem
dependências: o que está no repositório é exatamente o que vai para o ar.

## Rodar localmente

```bash
python3 -m http.server 8000
# abre http://localhost:8000
```

## Estrutura

```
index.html                 página inteira (os ícones SVG ficam em <symbol> no topo)
style.css                  estilos e animações
assets/icons/              logos das tecnologias (Devicon, baixados — funcionam offline)
assets/images/             foto
assets/*.pdf               currículos (PT e EN)
vercel.json                cabeçalhos de cache
```

## Trocar o currículo

Substitua o PDF em `assets/` mantendo o nome do arquivo. O cache está
configurado como `must-revalidate`, então a troca vale na hora — não é
preciso esperar cache expirar.

## Design

O conceito é o **degradê**: em português a mesma palavra nomeia o corte do
barbeiro e o gradiente. Daí saem os dois elementos visuais do site — o
divisor de seções (traços que rareiam da esquerda para a direita) e a
revelação do nome na home, em que um fio passa como uma navalha e o nome
aparece no rastro.

Paleta: [Kanagawa Wave](https://github.com/rebelot/kanagawa.nvim).
Tipografia: Bricolage Grotesque (títulos) e Instrument Sans (texto).
