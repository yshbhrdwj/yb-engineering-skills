# Design foundations

Platform-neutral principles. Web-specific mechanics live in the other references. Read once per Mode 4 task, not per page; outputs link the project design document rather than restating this file.

## Philosophy

**Purpose first.** Every decision serves an audience completing a task. Settle who uses it, how often, under what pressure, and what they must trust before choosing anything visual. Hierarchy, readability, feedback, and accessibility come before style. A beautiful site that is hard to use has failed.

**Distinctive, not generic.** These are signals to scrutinize, never bans: gradient-heavy backgrounds, glassmorphism, oversized rounded cards everywhere, repetitive three-column grids, purple SaaS dashboards, decorative icons, heavy shadows, giant headings with no hierarchy beneath them, purposeless empty space, and animation that delays the task. Each is acceptable only when it expresses the product's identity or serves its content. Ask of each choice: would this exact treatment fit a competitor in another industry? If yes, it is a default, not a decision.

**Craft at the detail level.** Quality lives in optical alignment, baseline rhythm, weight distribution, tracking and leading, icon geometry, consistent radii and borders, container widths, surface separation, button proportion, form alignment, density, and motion quality. Valid CSS and a rendering component are not evidence of finished design.

**Fit the product.** Derive expression from industry, audience, content type, usage frequency, brand, accessibility needs, and stack. Never impose one aesthetic across products. Never apply landing-page composition to a data application, or enterprise density to a consumer site.

**Systems over patches.** A defect seen on one page is usually a token or shared-component defect. Correct it at the source. Preserve approved decisions; never regenerate a design system per page.

## Hierarchy

The reader should know within seconds what this is, what matters most, and what to do next. Build hierarchy with as few signals as possible, in this order of cost: position and grouping, then size, then weight, then color, then decoration. Using all five at once flattens the result, because everything becomes loud. One dominant element per view; secondary information steps down one signal at a time. Proximity carries relationship: space within a group must be visibly smaller than space between groups, roughly half or less, or the grouping reads as accidental.

Cognitive load falls when similar things look alike and different things look different. A visual difference that carries no meaning is noise; a meaningful difference with no visual signal is a trap.

## Typography theory

Type is the interface for most content. Size sets reading distance and importance; weight sets emphasis; leading sets comfort; measure sets reading speed. Body text optimizes for sustained reading (moderate size, generous leading, 45–75 characters per line). Display text optimizes for recognition (larger, tighter leading, often tighter tracking, because the eye perceives letter gaps as wider at large sizes). Small text needs the opposite: slightly looser tracking and more weight. A scale is a set of roles, not a list of sizes: define each step by what it is for.

## Color science

Perceived lightness is not linear in sRGB hex or HSL: two HSL colors with equal "lightness" can differ sharply in perceived brightness (yellow versus blue). Build ramps in a perceptual space such as OKLCH, where equal lightness steps look equal, then check contrast on actual pairs. Hue carries identity, lightness carries hierarchy and contrast, chroma carries emphasis. Saturated color is an attention budget; spend it on what users must notice. Color never carries meaning alone: pair it with shape, text, position, or iconography.

## Spacing and geometry

A spacing scale is a vocabulary of relationships. Use a small geometric or near-geometric set (for example 4, 8, 12, 16, 24, 32, 48, 64) so differences are perceptible; steps closer than about 25% read as mistakes. Derive component padding from content: control height follows the line-height of its label plus vertical padding, so buttons and inputs that sit side by side share a height token.

Optical beats mathematical. The eye judges mass, not bounding boxes: a play triangle centered by its box looks left-heavy and needs nudging toward its point; round and pointed glyphs overshoot flat ones; text in a button with only lowercase and no descenders looks high when padding is symmetric; an icon beside text aligns to the cap height or x-height center, not the line box. Make such corrections once, in the component, with a comment explaining the optical reason.

Consistency is a system property. Radii, border widths, and shadow levels belong to small sets; nested radii follow outer radius = inner radius + gap so curves stay concentric.

## Feedback

Every action gets a response proportional to its consequence and latency: immediate state change for direct manipulation, a pending state when work takes noticeable time, explicit confirmation for consequential outcomes, and a recoverable error that preserves the user's work. Silence after an action is a defect. Feedback that steals focus or moves layout is its own defect.

## Accessibility principles

Design for people who use keyboards, screen readers, magnification, voice control, reduced motion, high contrast, and translation, and for people under stress, fatigue, or low literacy. The design decides most of this: structure and reading order, focus visibility, contrast, target size, labels and errors, motion, and plain language. Conformance is a separate, testable claim against a named standard; good principles do not establish it.
