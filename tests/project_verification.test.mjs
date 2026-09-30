import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const rootDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const frontendDir = path.join(rootDir, 'frontend');
const documentsDir = path.join(frontendDir, 'assets', 'documents');
const generatedDocsDir = path.join(frontendDir, 'assets', 'generated_docs');
const html = fs.readFileSync(path.join(frontendDir, 'index.html'), 'utf8');

function sectionById(id) {
    const match = html.match(new RegExp(`<section\\b[^>]*\\bid="${id}"[^>]*>[\\s\\S]*?<\\/section>`, 'i'));
    return match?.[0] ?? '';
}

test('La página principal es accesible y tiene una navegación corta', () => {
    assert.match(html, /<html\s+lang="es-CO"/i);
    assert.equal((html.match(/<h1\b/g) ?? []).length, 1);
    assert.match(html, /href="#contenido"[^>]*>Saltar al contenido/i);
    assert.match(html, /<main\b[^>]*id="contenido"/i);
    assert.match(html, /<details\b[^>]*class="mobile-menu"/i);
    assert.match(html, /<summary\b[^>]*>Menú<\/summary>/i);

    const navIds = [...html.matchAll(/<nav\b[^>]*aria-label="[^"]+"/g)];
    assert.ok(navIds.length >= 2, 'Debe ofrecer navegación para escritorio y móvil');
    assert.doesNotMatch(html, /cdn\.tailwindcss|fontawesome|fonts\.googleapis|app\.js|tailwind\.config\.js/i);
});

test('Los enlaces internos y los recursos publicados sí existen', () => {
    const ids = new Set([...html.matchAll(/\bid="([^"]+)"/g)].map((match) => match[1]));
    const internalLinks = [...html.matchAll(/href="#([^"]+)"/g)].map((match) => match[1]);
    for (const id of internalLinks) assert.ok(ids.has(id), `El enlace #${id} debe tener destino`);

    const localLinks = [...html.matchAll(/href="(assets\/[^"]+)"/g)].map((match) => match[1]);
    for (const link of localLinks) {
        assert.ok(fs.existsSync(path.join(frontendDir, link)), `Debe existir ${link}`);
    }
    assert.deepEqual(
        localLinks.filter((link) => /\.(?:docx|xlsx)$/i.test(link)).sort(),
        [
            'assets/documents/Evaluacion_Participantes_CGAO_Skills.xlsx',
            'assets/documents/Reto_ejemplo_aprendiz_ADSO_CGAO_Skills.docx',
        ],
        'La página publica el reto Word y la plantilla Excel como sus únicos documentos descargables',
    );
});

test('El cronograma concentra las fechas oficiales del evento', () => {
    const agenda = sectionById('agenda');
    assert.ok(agenda, 'Debe existir una sola sección de agenda');
    assert.match(agenda, /12\s*(?:al|–|-)\s*23 de octubre de 2026/i);
    assert.match(agenda, /26 de octubre de 2026/i);
    assert.match(agenda, /solo el 26 de octubre/i);
    assert.match(agenda, /29 de octubre de 2026/i);
    assert.doesNotMatch(agenda, /28 de octubre/i);
    assert.equal((html.match(/id="agenda"/g) ?? []).length, 1);
    assert.doesNotMatch(html, /id="ruta"|contador regresivo/i);
});

test('La evaluación distingue la regla general de la rúbrica de ejemplo ADSO', () => {
    const evaluation = sectionById('evaluacion');
    assert.ok(evaluation, 'Debe existir una sección de evaluación');
    for (const value of ['M', 'J', 'P']) assert.match(evaluation, new RegExp(`\\b${value}\\b`));
    assert.match(evaluation, /69\s*(?:puntos|%)/i);
    assert.match(evaluation, /23\s*(?:puntos|%)/i);
    assert.match(evaluation, /8\s*(?:puntos|%)/i);
    assert.match(evaluation, /reto de ejemplo/i);
    assert.match(evaluation, /sostenibilidad/i);
    assert.match(evaluation, /cierre y uso eficiente de la estación/i);
    assert.match(evaluation, /blanco para aprovechables limpios y secos/i);
    assert.match(evaluation, /verde para orgánicos aprovechables/i);
    assert.match(evaluation, /negro para no aprovechables/i);
    assert.match(evaluation, /resolución 2184 de 2019/i);

});

test('La web no simula inscripciones, resultados, cifras de impacto ni contactos', () => {
    assert.doesNotMatch(html, /<form\b|registration-form|Enviar inscripción|¡Inscribir talento/i);
    assert.doesNotMatch(html, /Cargando resultados|Resultados en vivo|200\+|Participantes esperados/i);
    assert.doesNotMatch(html, /mailto:|tel:|@cgao\.edu\.co|facebook\.com|instagram\.com/i);
    assert.match(html, /no recibe inscripciones/i);
    for (const base of [frontendDir]) {
        for (const relativePath of [
            'js/app.js',
            'js/content.js',
            'js/tailwind.config.js',
            'assets/data/results.json',
        ]) {
            assert.equal(
                fs.existsSync(path.join(base, relativePath)),
                false,
                `No debe quedar el archivo obsoleto ${relativePath}`,
            );
        }
    }
});

test('El centro de recursos publica una sola copia de cada archivo principal', () => {
    const resources = sectionById('recursos');
    assert.ok(resources, 'Debe existir un centro de recursos');
    for (const filename of [
        'Reto_ejemplo_aprendiz_ADSO_CGAO_Skills.docx',
        'Evaluacion_Participantes_CGAO_Skills.xlsx',
    ]) {
        const matches = [...resources.matchAll(new RegExp(`href="assets/documents/${filename.replaceAll('.', '\\.') }"`, 'g'))];
        assert.equal(matches.length, 1, `${filename} debe aparecer una sola vez`);
    }
    assert.doesNotMatch(resources, /\.pdf|\.csv/i);
    assert.doesNotMatch(html, /id="resultados"|id="evaluacion-participantes"|id="inscribir"/i);
});

test('La página principal publica el reto Word y la plantilla Excel con contenido válido', () => {
    const wordFile = path.join(documentsDir, 'Reto_ejemplo_aprendiz_ADSO_CGAO_Skills.docx');
    const excelFile = path.join(documentsDir, 'Evaluacion_Participantes_CGAO_Skills.xlsx');
    assert.ok(fs.existsSync(wordFile), 'Debe existir el reto Word');
    assert.ok(fs.existsSync(excelFile), 'Debe existir la plantilla Excel');
    assert.ok(fs.statSync(wordFile).size > 1000, 'El reto Word debe tener contenido');
    assert.ok(fs.statSync(excelFile).size > 1000, 'La plantilla Excel debe tener contenido');
});
test('El manual y el PDF de rúbrica se generan con la distribución y sostenibilidad actuales', () => {
    for (const filename of [
        'Rubrica_Maestra_Template.pdf',
        'Manual_Sostenibilidad_y_Etica.pdf',
        'Guia_Tecnica_Diseno_Prueba.pdf',
        'Checklist_Jueces_Dia0.pdf',
    ]) {
        const filepath = path.join(generatedDocsDir, filename);
        assert.ok(fs.existsSync(filepath), `Debe existir ${filename}`);
        assert.ok(fs.statSync(filepath).size > 500, `${filename} debe tener contenido`);
    }

    const manual = fs.readFileSync(path.join(documentsDir, 'Manual_Sostenibilidad_y_Etica.md'), 'utf8');
    assert.match(manual, /cierre y uso eficiente de la estación/i);
    assert.match(manual, /5\s*%.*10\s*%/s);
    assert.match(manual, /Resolución 2184 de 2019/);
    assert.match(manual, /artículo 4/i);
    assert.match(manual, /cada reto debe precisar sus propias evidencias/i);
});


