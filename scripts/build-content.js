const fs = require('fs')
const path = require('path')

const contentDir = path.join(__dirname, '..', 'content', 'events')
const outFile = path.join(__dirname, '..', 'src', 'data', 'event-content.json')

const result = {}

if (fs.existsSync(contentDir)) {
  const dirs = fs.readdirSync(contentDir)
  for (const dir of dirs) {
    const dirPath = path.join(contentDir, dir)
    if (!fs.statSync(dirPath).isDirectory()) continue
    
    const entry = {}
    for (const file of fs.readdirSync(dirPath)) {
      const filePath = path.join(dirPath, file)
      const content = fs.readFileSync(filePath, 'utf8')
      
      if (file.endsWith('.md')) {
        // Strip frontmatter
        const stripped = content.replace(/^---[\s\S]*?---\n*/, '')
        entry[file.replace('.md', '')] = stripped
      } else if (file.endsWith('.json')) {
        entry[file.replace('.json', '')] = JSON.parse(content)
      }
    }
    result[dir] = entry
  }
}

fs.writeFileSync(outFile, JSON.stringify(result, null, 2))
console.log(`Built content for ${Object.keys(result).length} events`)
