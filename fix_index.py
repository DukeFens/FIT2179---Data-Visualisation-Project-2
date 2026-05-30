import re

with open('index.html', 'r') as f:
    html = f.read()

replacements = [
    (
        r'<span class="fig-num">Figure 1.</span> Life-expectancy gains vs. sedentary peers, eight sport categories. The social dimension of racket sports appears to drive the outsized longevity benefit.',
        r'<span class="fig-num">Figure 1.</span> Life-expectancy gains vs. sedentary peers, eight sport categories.'
    ),
    (
        r'<span class="fig-num">Figure 2.</span> Energy expenditure per hour, 70-kg adult.',
        r'<span class="fig-num">Figure 2.</span> Energy expenditure per hour.'
    ),
    (
        r'<span class="fig-num">Figure 3.</span> Muscle activation intensity \(% MVIC\) during a forehand overhead smash. Darker green = higher activation.',
        r'<span class="fig-num">Figure 3.</span> Muscle activation intensity during a forehand overhead smash.'
    ),
    (
        r'<span class="fig-num">Figure 4.</span> Interactive state dashboard: choropleth map with linked line rank, area rate trend, and stacked bar by era. State splits 2016–2024 estimated from national AusPlay totals.',
        r'<span class="fig-num">Figure 4.</span> Interactive state dashboard.'
    ),
    (
        r'<span class="fig-num">Figure 5 ·</span> National adult participation by gender, 2016–2025. Area band = gap between male and female participation; dashed line marks 2024 AusPlay methodology revision.',
        r'<span class="fig-num">Figure 5 ·</span> National adult participation by gender, 2016–2025.'
    ),
    (
        r'<span class="fig-num">Figure 6 ·</span> Participation % by age group and gender. The young-adult skew is consistent across years but intensifying.',
        r'<span class="fig-num">Figure 6 ·</span> Participation % by age group and gender.'
    ),
    (
        r'<span class="fig-num">Figure 7 ·</span> Badminton courts by Greater Melbourne LGA \(circle size\), shaded by Asian-born residents \(%\).',
        r'<span class="fig-num">Figure 7 ·</span> Badminton courts by Greater Melbourne LGA.'
    ),
    (
        r'<span class="fig-num">Figure 8 ·</span> Melbourne LGAs: Asian-born % \(2021 Census\) vs. badminton courts. Dot size = LGA population; trend line shows positive correlation.',
        r'<span class="fig-num">Figure 8 ·</span> Asian-born population vs. badminton courts by LGA.'
    ),
    (
        r'<span class="fig-num">Figure 9 ·</span> Logarithmic drop-off across competitive tiers.',
        r'<span class="fig-num">Figure 9 ·</span> Talent pipeline drop-off across competitive tiers.'
    ),
    (
        r'<span class="fig-num">Figure 10 ·</span> Australian Open titles by nation, 2010–2024. Use the dropdown to filter by discipline.',
        r'<span class="fig-num">Figure 10 ·</span> Australian Open titles by nation, 2010–2024.'
    ),
    (
        r'<span class="fig-num">Figure 11 ·</span> BWF world ranking history, 2022–2025. Lower values = higher rankings.',
        r'<span class="fig-num">Figure 11 ·</span> BWF world ranking trajectories, 2022–2025.'
    ),
    (
        r'<span class="fig-num">Figure 12 ·</span> Australian-hosted BWF events, 2016–2025. Bubble size = total entries; colour = tournament grade.',
        r'<span class="fig-num">Figure 12 ·</span> Australian-hosted BWF events, 2016–2025.'
    ),
    (
        r'Primary sources: AusPlay 2025 \(Australian Sports Commission\) · Badminton Australia Annual Report 2023/24 · BWF Historical Rankings · Badminton Victoria Club Directory · Copenhagen City Heart Study \(Schnohr et al., 2018\) · Compendium of Physical Activities \(Ainsworth et al., 2011\) · Frontiers in Sports and Active Living \(2025\).',
        r'Primary sources: AusPlay 2016-2025 (Australian Sports Commission) · ABS 2021 Census · ABS Population Estimates · Badminton Australia Annual Report 2023/24 · BWF Historical Rankings & Tournament Software · Badminton Victoria Club Directory · Copenhagen City Heart Study (Schnohr et al., 2018) · Compendium of Physical Activities (Ainsworth et al., 2011) · Frontiers in Sports and Active Living (2025).'
    )
]

for target, repl in replacements:
    html = re.sub(target, repl, html)

with open('index.html', 'w') as f:
    f.write(html)

print("Done")
