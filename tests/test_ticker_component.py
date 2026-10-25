"""
Test for Legal Metrology Advisories & Public Notices Ticker UI Modernization
and Material You Theme Color Palette Popover Overhaul.
"""
import unittest
from fastapi.testclient import TestClient
from backend.api.main import app


class TestNoticeTickerAndThemePickerModernization(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_indicator_dots_completely_removed_from_dom(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.text

        # Verify indicator dots container and dot elements are absent from DOM
        self.assertNotIn("tickerDotsContainer", html, "tickerDotsContainer must be completely removed from DOM")
        self.assertNotIn("ticker-dot", html, "ticker-dot classes must be completely removed from DOM")

    def test_clean_layout_and_controls_glassmorphic_styling(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.text

        # Verify notice ticker title and pause/play button presence
        self.assertIn("LEGAL METROLOGY ADVISORIES & PUBLIC NOTICES", html)
        self.assertIn("btnToggleTickerPause", html)

        # Verify glassmorphic dark-mode styling on controls pill
        self.assertIn("backdrop-filter: blur(16px)", html)
        self.assertIn("background: rgba(15, 23, 42, 0.6)", html)
        self.assertIn("border: 1px solid rgba(255, 255, 255, 0.08)", html)

    def test_theme_color_picker_popover_and_triggers_in_both_places(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.text

        # Place 1: Top Navigation Strip Trigger
        self.assertIn("headerThemePickerBtn", html)
        self.assertIn("headerCurrentThemePreview", html)
        self.assertIn("toggleThemeColorPicker(event, 'header')", html)

        # Place 2: Workbench Sidebar Trigger
        self.assertIn("sidebarThemePickerBtn", html)
        self.assertIn("sidebarCurrentThemePreview", html)
        self.assertIn("toggleThemeColorPicker(event, 'sidebar')", html)

        # Popover & Backdrop
        self.assertIn("themeColorPickerPopover", html)
        self.assertIn("themeColorPickerBackdrop", html)
        self.assertIn("Pick a theme color", html)

        # 15 Multi-tone Palettes
        expected_palettes = [
            'classic-blue', 'cool-grey', 'navy-blue', 'steel-blue', 'sage-teal',
            'teal-cyan', 'forest-green', 'olive-green', 'olive-gold', 'tangerine-orange',
            'warm-brown', 'ruby-crimson', 'rose-mauve', 'berry-magenta', 'purple-violet'
        ]
        for p in expected_palettes:
            self.assertIn(f'data-theme-key="{p}"', html)

        # Custom eyedropper input
        self.assertIn("themeNativeColorInput", html)
        self.assertIn("triggerCustomColorPicker(event)", html)

    def test_dynamic_theme_background_color_change(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.text

        # Verify dynamic background color variables and style rules
        self.assertIn("--theme-bg", html)
        self.assertIn("--theme-surface", html)
        self.assertIn("--theme-card", html)
        self.assertIn("--theme-border", html)
        self.assertIn("generateCustomBackgrounds", html)

        # Verify background override applied to body and containers
        self.assertIn("body:not(.theme-emerald)", html)
        self.assertIn("document.body.style.backgroundColor = palette.bg", html)
        self.assertIn('[class*="bg-slate-950"]', html)
        self.assertIn('[class*="bg-slate-900"]', html)

    def test_warehouse_hero_banner_and_whats_new_ticker_matching_screenshot(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.text

        # 1. Warehouse Sovereign Banner & "For Video Click Here" button
        self.assertIn("ministryWarehouseHeroBanner", html)
        self.assertIn("warehouse_banner.png", html)
        self.assertIn("For Video Click Here", html)
        self.assertIn("openVideoDemoModal()", html)

        # 2. What's New Ticker with Pause Button & Continuous Marquee
        self.assertIn("What's New", html)
        self.assertIn("marquee-track-container", html)
        self.assertIn("marquee-track-content", html)
        self.assertIn("btnToggleTickerPause", html)
        self.assertIn("Imposition of sugar mill wise stock holding limit order", html)
        self.assertIn("Format: PDF, Language: English, Size: 11.1MB", html)

        # 3. View All Button and Modals
        self.assertIn("openAllNoticesModal()", html)
        self.assertIn("allNoticesModal", html)
        self.assertIn("portalVideoDemoModal", html)

        # 4. Verify warehouse banner asset is actively served with 200 OK
        img_res = self.client.get("/icons/warehouse_banner.png")
        self.assertEqual(img_res.status_code, 200)

    def test_global_theme_engine_tokens_and_multi_mode_synchronization(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.text

        # 1. High-contrast theme tokens in root / dark mode
        self.assertIn("--bg-primary: #0b0f19", html)
        self.assertIn("--surface-card: rgba(15, 23, 42, 0.75)", html)
        self.assertIn("--text-primary: #ffffff", html)
        self.assertIn("--text-secondary: #94a3b8", html)
        self.assertIn("--border-color: rgba(255, 255, 255, 0.08)", html)

        # 2. High-contrast theme tokens in light mode
        self.assertIn("--bg-primary: #f8fafc", html)
        self.assertIn("--surface-card: #ffffff", html)
        self.assertIn("--text-primary: #0f172a", html)
        self.assertIn("--text-secondary: #475569", html)
        self.assertIn("--border-color: rgba(0, 0, 0, 0.08)", html)

        # 3. ThemeContext state machine and listener
        self.assertIn("window.ThemeContext = ThemeContext", html)
        self.assertIn("prefers-color-scheme: dark", html)
        self.assertIn("handleSystemThemeChange", html)
        self.assertIn("addEventListener", html)

        # 4. Root data-theme attribute and persistence
        self.assertIn('html.setAttribute("data-theme", resolved)', html)
        self.assertIn('localStorage.setItem("theme", mode)', html)
        self.assertIn('localStorage.setItem("precisionx_theme_mode", mode)', html)

        # 5. Three states: light, dark, system
        self.assertIn("theme-btn-light", html)
        self.assertIn("theme-btn-dark", html)
        self.assertIn("theme-btn-system", html)
        self.assertIn("setThemeMode('light')", html)
        self.assertIn("setThemeMode('dark')", html)
        self.assertIn("setThemeMode('system')", html)

    def test_header_user_profile_card_flexbox_and_glassmorphism(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.text

        # 1. Top-Left Profile Card Container
        self.assertIn('id="headerUserProfileCard"', html)

        # 2. Flexbox alignment & nowrap properties
        self.assertIn("display: flex; align-items: center; gap: 0.75rem; flex-wrap: nowrap;", html)

        # 3. Glassmorphic Surface & Border Refinement tokens
        self.assertIn("background: var(--surface-card); backdrop-filter: blur(16px); border: 1px solid var(--border-color); border-radius: 12px; padding: 0.5rem 0.75rem;", html)

        # 4. Avatar, badge ID and role elements
        self.assertIn('id="headerUserAvatar"', html)
        self.assertIn('id="headerUserName"', html)
        self.assertIn('id="headerOfficerBadge"', html)
        self.assertIn('id="headerUserRole"', html)
        self.assertIn("GOV-IN-7842", html)

    def test_inspector_auth_card_glassmorphism_and_gap_spacing(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.text

        # 1. Upper Notice Ticker Positioning directly above authentication container
        ticker_pos = html.find('id="ministryNoticeTickerContainer"')
        auth_pos = html.find('id="inspectorAuthContainer"')
        self.assertNotEqual(ticker_pos, -1)
        self.assertNotEqual(auth_pos, -1)
        self.assertLess(ticker_pos, auth_pos, "Notice ticker must be positioned directly above authentication box")

        # 2. Glassmorphic card styling on inspector sign-in card
        self.assertIn('id="inspectorAuthCard"', html)
        self.assertIn("background: var(--surface-card); backdrop-filter: blur(16px); border: 1px solid var(--border-color); border-radius: 16px; padding: 2rem;", html)

        # 3. Flawless form controls with gap: 1rem spacing
        self.assertIn("display: flex; flex-direction: column; gap: 1rem;", html)
        self.assertIn('id="roleTab-INSPECTOR"', html)
        self.assertIn('id="roleTab-CITIZEN"', html)
        self.assertIn('id="roleTab-TRADER"', html)
        self.assertIn('id="formInspectorLogin"', html)
        self.assertIn('id="btnLoginSubmit"', html)

    def test_ad_banner_carousel_with_left_right_controls_and_slides(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.text

        # 1. 4 Carousel Ad Slides in HTML & JS engine
        self.assertIn("ad_slide_1.png", html)
        self.assertIn("ad_slide_2.png", html)
        self.assertIn("ad_slide_3.png", html)
        self.assertIn("ad_slide_4.png", html)

        # 2. Left & Right clickable controls
        self.assertIn("showPrevWarehouseSlide()", html)
        self.assertIn("showNextWarehouseSlide()", html)
        self.assertIn("setAdSlide(", html)

        # 3. Slide indicators and pause controls
        self.assertIn("adSlideDot-0", html)
        self.assertIn("adSlideDot-1", html)
        self.assertIn("adSlideDot-2", html)
        self.assertIn("adSlideDot-3", html)
        self.assertIn("btnWarehouseBannerPause", html)

        # 4. Verify all 4 images are served with 200 OK
        for i in range(1, 5):
            img_res = self.client.get(f"/icons/ad_slide_{i}.png")
            self.assertEqual(img_res.status_code, 200, f"ad_slide_{i}.png must return HTTP 200")

    def test_what_is_precisionx_overview_section_matching_screenshot(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.text

        # 1. Overview Section Container
        self.assertIn('id="whatIsPrecisionXSection"', html)

        # 2. Branding & Badges
        self.assertIn("PrecisionX Sovereign Verification Gateway", html)
        self.assertIn("R-76 SOVEREIGN", html)
        self.assertIn("National Legal Metrology Verification Gateway (विधिक मापविज्ञान प्रभाग)", html)
        self.assertIn("Statutory compliance for Non-Automatic Weighing Instruments (NAWI)", html)

        # 3. 4 Pillars with INFO badges
        self.assertIn("OIML R-76 MPE Engine", html)
        self.assertIn("Ed25519 Cryptography", html)
        self.assertIn("PTB DCC & PDF/A-3", html)
        self.assertIn("WELMEC 7.2 LRS Sealing", html)
        self.assertIn("INFO ℹ️", html)

        # 4. Statutory Disclosure Box
        self.assertIn("STATUTORY DISCLOSURE (SEC. 44, LM ACT 2009)", html)
        self.assertIn("Restricted to authorized enforcement officers & registered citizens", html)

        # 5. Positioned above inspector authentication box
        overview_pos = html.find('id="whatIsPrecisionXSection"')
        auth_pos = html.find('id="inspectorAuthContainer"')
        self.assertNotEqual(overview_pos, -1)
        self.assertNotEqual(auth_pos, -1)
        self.assertLess(overview_pos, auth_pos, "whatIsPrecisionXSection must be positioned directly above inspectorAuthContainer")

    def test_precisionx_milestones_banner_matching_screenshot(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.text

        # 1. Milestones Container
        self.assertIn('id="precisionxMilestonesBanner"', html)
        self.assertIn("PRECISIONX MILESTONES", html)

        # 2. Dynamic Metric IDs preserved
        self.assertIn('id="heroStatVerified"', html)
        self.assertIn('id="heroStatInspectors"', html)
        self.assertIn('id="heroStatCompliance"', html)
        self.assertIn('id="heroStatViolations"', html)
        self.assertIn("WELMEC 7.2 LRS Integrity", html)

        # 3. Positioned directly below authentication box
        auth_pos = html.find('id="inspectorAuthContainer"')
        milestones_pos = html.find('id="precisionxMilestonesBanner"')
        self.assertNotEqual(auth_pos, -1)
        self.assertNotEqual(milestones_pos, -1)
        self.assertLess(auth_pos, milestones_pos, "precisionxMilestonesBanner must be positioned directly below inspectorAuthContainer")

    def test_neon_red_theme_palette_present_and_configured(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.text

        # Verify neon-red is defined in THEME_PALETTES
        self.assertIn('"neon-red":', html)
        self.assertIn('"#ff003f"', html)
        self.assertIn('"#000000"', html)
        self.assertIn('"#00d2ff"', html)
        self.assertIn('data-theme-key="neon-red"', html)
        self.assertIn('title="Neon Red (Black & Blue)"', html)


if __name__ == "__main__":
    unittest.main()
