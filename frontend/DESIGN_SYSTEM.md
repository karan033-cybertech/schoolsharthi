# SchoolSharthi Design System

## 🎨 Color Palette

### Primary Colors
```css
Primary Blue:   #0284c7 (Primary-600)
Purple:         #7c3aed (Purple-600)  
Pink:           #ec4899 (Pink-600)
```

### Gradients by Feature
- **Notes**: Blue → Cyan (`from-blue-500 to-cyan-500`)
- **PYQs**: Green → Emerald (`from-green-500 to-emerald-500`)
- **AI Doubt**: Purple → Pink (`from-purple-500 to-pink-500`)
- **Study Assistant**: Indigo → Purple (`from-indigo-500 to-purple-500`)
- **Career**: Orange → Red (`from-orange-500 to-red-500`)

### Semantic Colors
- **Success**: Green-500 (`#22c55e`)
- **Warning**: Yellow-400 (`#facc15`)
- **Error**: Red-500 (`#ef4444`)
- **Info**: Blue-500 (`#3b82f6`)

---

## 📐 Typography Scale

### Headings
- **H1 (Hero)**: `text-5xl md:text-7xl` - Bold, Gradient
- **H2 (Section)**: `text-4xl md:text-5xl` - Bold, Gradient
- **H3 (Card Title)**: `text-2xl` - Bold
- **H4 (Subsection)**: `text-xl` - Semibold

### Body Text
- **Large**: `text-lg` - 18px
- **Base**: `text-base` - 16px (default)
- **Small**: `text-sm` - 14px
- **Tiny**: `text-xs` - 12px

### Font Weights
- **Extrabold**: `font-extrabold` (900) - Headlines
- **Bold**: `font-bold` (700) - Titles
- **Semibold**: `font-semibold` (600) - Subtitles
- **Medium**: `font-medium` (500) - Emphasis
- **Regular**: `font-normal` (400) - Body

---

## 🎭 Animation Guidelines

### Duration
- **Fast**: 200ms - Button clicks, toggles
- **Medium**: 300-500ms - Card hovers, transitions
- **Slow**: 600-1000ms - Page loads, complex animations

### Easing
- **Default**: `ease-in-out` - Most transitions
- **Bounce**: `ease-out` - Entrances
- **Smooth**: `cubic-bezier(0.4, 0, 0.2, 1)` - Premium feel

### Transform Effects
- **Lift**: `hover:-translate-y-2` - Cards
- **Scale**: `hover:scale-105` - Buttons, icons
- **Rotate**: `hover:rotate-6` - Icons (subtle)

---

## 🎯 Component Patterns

### Cards
```tsx
// Base Structure
<div className="bg-white rounded-2xl shadow-lg hover:shadow-2xl 
                transition-all duration-300 hover:-translate-y-2 
                border border-gray-100">
  {/* Icon with gradient background */}
  {/* Title */}
  {/* Description */}
  {/* CTA */}
</div>
```

### Buttons
```tsx
// Primary Button
<button className="px-8 py-4 bg-gradient-to-r from-primary-600 
                  to-purple-600 text-white rounded-full font-bold 
                  hover:shadow-2xl hover:scale-105 transition-all">
  Button Text
</button>

// Secondary Button
<button className="px-8 py-4 bg-white text-primary-600 rounded-full 
                  font-bold border-2 border-primary-600 
                  hover:bg-primary-50 transition-all">
  Button Text
</button>
```

### Badges
```tsx
// Status Badge
<span className="px-3 py-1 bg-gradient-to-r from-yellow-400 
                to-orange-500 text-white text-xs font-bold 
                rounded-full shadow-lg">
  New
</span>
```

---

## 📱 Spacing System

### Padding
- **Tight**: `p-4` (16px)
- **Normal**: `p-6` (24px)
- **Comfortable**: `p-8` (32px)
- **Spacious**: `p-12` (48px)

### Gaps
- **Small**: `gap-2` (8px)
- **Medium**: `gap-4` (16px)
- **Large**: `gap-6` (24px)
- **XL**: `gap-8` (32px)

### Margins
- **Section**: `py-16 md:py-20` (64-80px)
- **Card**: `mb-6` (24px)
- **Text**: `mb-4` (16px)

---

## 🎨 Visual Effects

### Shadows
- **Small**: `shadow-sm` - Subtle depth
- **Medium**: `shadow-lg` - Cards
- **Large**: `shadow-2xl` - Hover states
- **Colored**: `shadow-primary-500/50` - Accent shadows

### Blur
- **Backdrop**: `backdrop-blur-md` - Glass effect
- **Background**: `blur-xl` - Decorative elements

### Gradients
- **Text**: `bg-gradient-to-r from-primary-600 to-purple-600 bg-clip-text text-transparent`
- **Background**: `bg-gradient-to-br from-primary-500 to-purple-500`
- **Border**: Gradient borders via pseudo-elements

---

## 🎯 Accessibility

### Touch Targets
- Minimum: `44x44px` (iOS/Android guidelines)
- Buttons: `min-h-[44px] min-w-[44px]`

### Focus States
```css
focus:ring-2 focus:ring-primary-500 focus:outline-none
```

### Color Contrast
- Text on white: WCAG AA compliant
- Gradient text: High contrast backgrounds
- Interactive elements: Clear visual feedback

---

## 📐 Layout Patterns

### Container
```tsx
<div className="container mx-auto px-4">
  {/* Content */}
</div>
```

### Grid
```tsx
// Responsive Grid
<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* Cards */}
</div>
```

### Flex
```tsx
// Centered Content
<div className="flex items-center justify-center gap-4">
  {/* Items */}
</div>
```

---

## 🎨 Icon Guidelines

### Size
- **Small**: `w-4 h-4` (16px) - Inline text
- **Medium**: `w-6 h-6` (24px) - Buttons
- **Large**: `w-8 h-8` (32px) - Cards
- **XL**: `w-12 h-12` (48px) - Hero sections

### Library
- **Lucide React**: Primary icon library
- **Emojis**: For personality and visual interest

---

## 🚀 Performance Tips

1. **Use CSS transforms** instead of position changes
2. **Lazy load images** with `loading="lazy"`
3. **Debounce scroll events** for animations
4. **Use `will-change`** sparingly for animated elements
5. **Optimize gradients** - avoid too many stops

---

## 📱 Mobile Considerations

- **Touch-friendly**: Large tap targets
- **Readable**: Minimum 16px font size
- **Fast**: Optimized animations
- **Simple**: Reduced complexity on small screens

---

Made with ❤️ for SchoolSharthi
