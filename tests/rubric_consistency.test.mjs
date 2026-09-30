import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const rootDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const documentsDir = path.join(rootDir, 'frontend', 'assets', 'documents');
const csvText = fs.readFileSync(path.join(documentsDir, 'Rubrica_Maestra_Template.csv'), 'utf8').trim();

function parseCsvLine(line) {
    const cells = [];
    let value = '';
    let quoted = false;
    for (let index = 0; index < line.length; index += 1) {
        const character = line[index];
        if (character === '"' && quoted && line[index + 1] === '"') {
            value += '"';
            index += 1;
        } else if (character === '"') {
            quoted = !quoted;
        } else if (character === ',' && !quoted) {
            cells.push(value);
            value = '';
        } else {
            value += character;
        }
    }
    cells.push(value);
    return cells;
}

const rows = csvText.split(/\r?\n/).map(parseCsvLine);

test('La rúbrica suma 100 puntos y mantiene los módulos y la regla M-J-P', () => {
    const criteria = rows.slice(1);
    const ids = criteria.map((row) => row[0]);
    const expectedIds = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'J1', 'J2', 'J3', 'P1', 'P2'];
    const modules = { A: 0, B: 0, C: 0, D: 0 };
    const types = { M: 0, J: 0, P: 0 };

    assert.deepEqual(ids, expectedIds);
    for (const row of criteria) {
        const points = Number(row[5]);
        assert.ok(Number.isFinite(points), `Puntaje válido para ${row[0]}`);
        modules[row[1]] += points;
        types[row[4]] += points;
    }
    assert.deepEqual(modules, { A: 15, B: 60, C: 15, D: 10 });
    assert.deepEqual(types, { M: 69, J: 23, P: 8 });
    assert.equal(Object.values(modules).reduce((sum, points) => sum + points, 0), 100);
    assert.ok(types.M >= 60 && types.J <= 30 && types.P <= 10);
});

test('Los criterios del módulo D del reto de ADSO son observables y coherentes', () => {
    const criteria = Object.fromEntries(rows.slice(1).map((row) => [row[0], row]));
    const rubric = fs.readFileSync(path.join(documentsDir, 'Rubrica_Maestra_Template.md'), 'utf8').toLowerCase();
    const manual = fs.readFileSync(path.join(documentsDir, 'Manual_Sostenibilidad_y_Etica.md'), 'utf8').toLowerCase();

    assert.equal(criteria.M7[1], 'D');
    assert.equal(Number(criteria.M7[5]), 2);
    assert.match(`${criteria.M7[2]} ${criteria.M7[3]}`.toLowerCase(), /cierre y uso eficiente de la estación/);
    assert.match(`${criteria.M7[2]} ${criteria.M7[3]}`.toLowerCase(), /archivos temporales/);
    assert.match(`${criteria.M7[2]} ${criteria.M7[3]}`.toLowerCase(), /apaga el monitor o el equipo/);
    assert.equal(criteria.P1[1], 'D');
    assert.equal(Number(criteria.P1[5]), 4);
    assert.match(`${criteria.P1[2]} ${criteria.P1[3]}`.toLowerCase(), /ergonom/);
    assert.equal(criteria.P2[1], 'D');
    assert.equal(Number(criteria.P2[5]), 4);
    assert.match(`${criteria.P2[2]} ${criteria.P2[3]}`.toLowerCase(), /blanco para residuos aprovechables limpios y secos/);
    assert.match(`${criteria.P2[2]} ${criteria.P2[3]}`.toLowerCase(), /verde para residuos orgánicos aprovechables/);
    assert.match(`${criteria.P2[2]} ${criteria.P2[3]}`.toLowerCase(), /negro para residuos no aprovechables/);
    assert.match(rubric, /almacenamiento local/);
    assert.match(rubric, /orden descendente/);
    assert.match(rubric, /guía técnica define rangos generales/);
    assert.match(manual, /resolución 2184 de 2019/);
    assert.match(manual, /cierre y uso eficiente de la estación/);
    assert.match(manual, /cada reto debe precisar sus propias evidencias/);
    assert.doesNotMatch(rubric, /circuito serie|conexión de base de datos|50 ms|desperdicio < 5 %/i);
});

test('El reto Word y la plantilla Excel publicados corresponden a archivos válidos', () => {
    const files = [
        ['Reto_ejemplo_aprendiz_ADSO_CGAO_Skills.docx', 1000],
        ['Evaluacion_Participantes_CGAO_Skills.xlsx', 2000],
    ];
    for (const [filename, minSize] of files) {
        const filepath = path.join(documentsDir, filename);
        assert.ok(fs.existsSync(filepath), `Debe existir ${filename}`);
        assert.ok(fs.statSync(filepath).size > minSize, `${filename} debe tener contenido`);
    }
});
