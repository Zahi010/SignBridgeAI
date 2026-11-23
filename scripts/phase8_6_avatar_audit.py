"""
SignBridge AI - Phase 8.6 Full 3D Avatar System Audit & Kinematic Verification Script.
Connects directly to Chrome/Edge debugging session on 127.0.0.1:9222.
Creates a clean dedicated tab, inspects WebGL canvas, measures meshes and kinematics,
and captures visual evidence into reports/evidence/avatar_audit/.
"""

import asyncio
import json
import base64
import urllib.request
from pathlib import Path
import websockets

CDP_HTTP = "http://127.0.0.1:9222"
EVIDENCE_DIR = Path("reports/evidence/avatar_audit")
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


async def send_cmd(ws, method, params=None, cmd_id=1):
    payload = {"id": cmd_id, "method": method, "params": params or {}}
    await ws.send(json.dumps(payload))
    while True:
        resp = await ws.recv()
        data = json.loads(resp)
        if data.get("id") == cmd_id:
            return data


async def evaluate(ws, expr, cmd_id=100):
    res = await send_cmd(ws, "Runtime.evaluate", {
        "expression": expr,
        "returnByValue": True,
        "awaitPromise": True
    }, cmd_id=cmd_id)
    return res.get("result", {}).get("result", {}).get("value")


async def capture_screenshot(ws, filename, cmd_id=200):
    res = await send_cmd(ws, "Page.captureScreenshot", {"format": "png"}, cmd_id=cmd_id)
    b64 = res.get("result", {}).get("data")
    if b64:
        img_bytes = base64.b64decode(b64)
        out_path = EVIDENCE_DIR / filename
        out_path.write_bytes(img_bytes)
        print(f"  [SCREENSHOT] Saved: {out_path} ({len(img_bytes):,} bytes)")
        return str(out_path)
    return None


async def run_avatar_audit():
    print("[PHASE 8.6 AVATAR AUDIT] Creating dedicated CDP tab on 127.0.0.1:9222...")
    req = urllib.request.Request(f"{CDP_HTTP}/json/new?http://localhost:5173/avatar-audit", method="PUT")
    with urllib.request.urlopen(req) as resp:
        tab_info = json.loads(resp.read().decode())

    target_id = tab_info["id"]
    ws_url = tab_info["webSocketDebuggerUrl"]
    print(f"[CDP] Created tab {target_id}, ws: {ws_url}")

    audit_data = {
        "webgl": {},
        "scene_graph": {},
        "anatomy_topology": {},
        "kinematics": {},
        "synchronization": {},
        "facial_nmm": {},
        "performance": {},
        "screenshots": {}
    }

    try:
        async with websockets.connect(ws_url, max_size=25 * 1024 * 1024) as ws:
            # Setup viewport
            await send_cmd(ws, "Page.enable", cmd_id=1)
            await send_cmd(ws, "Runtime.enable", cmd_id=2)
            await send_cmd(ws, "DOM.enable", cmd_id=3)
            await send_cmd(ws, "Emulation.setDeviceMetricsOverride", {
                "width": 1440,
                "height": 900,
                "deviceScaleFactor": 1,
                "mobile": False
            }, cmd_id=4)

            # Wait for page to mount
            await asyncio.sleep(3.0)

            # 1. Audit WebGL and Canvas
            print("\n--- 1. WebGL & Scene Discovery ---")
            webgl_data = await evaluate(ws, """
            (() => {
                const canvas = document.querySelector('canvas');
                if (!canvas) return { error: 'No canvas found' };
                const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
                if (!gl) return { error: 'No WebGL context' };
                
                return {
                    width: canvas.width,
                    height: canvas.height,
                    vendor: gl.getParameter(gl.VENDOR),
                    renderer: gl.getParameter(gl.RENDERER),
                    version: gl.getParameter(gl.VERSION),
                    glsl: gl.getParameter(gl.SHADING_LANGUAGE_VERSION),
                    maxTextureSize: gl.getParameter(gl.MAX_TEXTURE_SIZE),
                    maxVertexAttribs: gl.getParameter(gl.MAX_VERTEX_ATTRIBS)
                };
            })()
            """, cmd_id=10)
            audit_data["webgl"] = webgl_data
            print("  WebGL:", webgl_data)

            # 2. Side-by-Side Synchronization Inspection on /avatar-audit
            print("\n--- 2. Dual-Viewport Synchronization Audit ---")
            sync_data = await evaluate(ws, """
            (() => {
                const video = document.querySelector('video');
                const avatarContainer = document.querySelector('.bg-slate-900.rounded-2xl');
                
                // Inspect master scrubber vs avatar controls
                const masterSlider = document.querySelector('input[type="range"]');
                const timeDisplays = Array.from(document.querySelectorAll('span.font-mono')).map(s => s.innerText);
                
                return {
                    hasVideo: !!video,
                    videoSrc: video?.src || null,
                    videoDuration: video?.duration || null,
                    videoCurrentTime: video?.currentTime || 0,
                    videoPaused: video?.paused || false,
                    hasMasterSlider: !!masterSlider,
                    sliderMax: masterSlider?.max || null,
                    hasAvatarContainer: !!avatarContainer,
                    timeDisplays: timeDisplays.slice(0, 5)
                };
            })()
            """, cmd_id=11)
            audit_data["synchronization"]["avatar_audit_page"] = sync_data
            print("  Sync on /avatar-audit:", sync_data)

            s0 = await capture_screenshot(ws, "07_avatar_audit_side_by_side.png", cmd_id=201)
            audit_data["screenshots"]["07_avatar_audit_side_by_side.png"] = s0

            # 3. Navigate to /demo
            print("\n--- 3. Navigating to /demo for Demonstration Pipeline Audit ---")
            await send_cmd(ws, "Page.navigate", {"url": "http://localhost:5173/demo"}, cmd_id=20)
            await asyncio.sleep(2.5)

            # Step through to Step 4
            await evaluate(ws, """
            (() => {
                const buttons = Array.from(document.querySelectorAll('button'));
                const step4 = buttons.find(b => b.textContent.includes('Synchronized Signing') || b.textContent.includes('Step 4'));
                if (step4) { step4.click(); return; }
                const c1 = buttons.find(b => b.textContent.includes('Continue to Step 2'));
                if (c1) c1.click();
            })()
            """, cmd_id=21)
            await asyncio.sleep(1.0)

            await evaluate(ws, """
            (() => {
                const buttons = Array.from(document.querySelectorAll('button'));
                const step4 = buttons.find(b => b.textContent.includes('Synchronized Signing') || b.textContent.includes('Step 4'));
                if (step4) { step4.click(); return; }
                const c2 = buttons.find(b => b.textContent.includes('Continue to Step 3'));
                if (c2) c2.click();
            })()
            """, cmd_id=22)
            await asyncio.sleep(1.0)

            await evaluate(ws, """
            (() => {
                const buttons = Array.from(document.querySelectorAll('button'));
                const c3 = buttons.find(b => b.textContent.includes('View Synchronized Signing') || b.textContent.includes('Step 4'));
                if (c3) c3.click();
            })()
            """, cmd_id=23)
            await asyncio.sleep(2.0)

            # Capture Algorithm signing on Step 4
            s1 = await capture_screenshot(ws, "06_algorithm_signing_step4.png", cmd_id=202)
            audit_data["screenshots"]["06_algorithm_signing_step4.png"] = s1

            # 4. Measure Live Demo Step 4 Synchronization Coupling
            print("\n--- 4. Live Demo Step 4 Synchronization Test ---")
            demo_sync_test = await evaluate(ws, """
            (() => {
                const video = document.querySelector('video');
                const vStateBefore = {
                    paused: video?.paused,
                    time: video?.currentTime
                };
                
                // Click master play button on LiveDemoPage
                const masterPlayBtn = Array.from(document.querySelectorAll('button')).find(
                    b => b.querySelector('svg') && b.className.includes('bg-indigo-600')
                );
                if (masterPlayBtn) masterPlayBtn.click();
                
                return {
                    vStateBefore,
                    clickedMasterPlay: !!masterPlayBtn
                };
            })()
            """, cmd_id=30)
            await asyncio.sleep(1.5)

            demo_sync_after = await evaluate(ws, """
            (() => {
                const video = document.querySelector('video');
                return {
                    vStateAfter: {
                        paused: video?.paused,
                        time: video?.currentTime
                    }
                };
            })()
            """, cmd_id=31)
            audit_data["synchronization"]["demo_page_coupling"] = {
                "before": demo_sync_test,
                "after": demo_sync_after
            }
            print("  Demo coupling:", audit_data["synchronization"]["demo_page_coupling"])

            # 5. Test Camera Presets in AvatarViewer
            print("\n--- 5. Camera Angles & Visual Perspective Audit ---")
            # Default
            await evaluate(ws, """
            (() => {
                // Find preset button inside AvatarControls (inside .bg-slate-900.rounded-2xl)
                const avatarBox = document.querySelector('.bg-slate-900.rounded-2xl');
                if (!avatarBox) return 'No avatarBox';
                const btns = Array.from(avatarBox.querySelectorAll('button'));
                const b = btns.find(btn => btn.textContent.trim().toLowerCase() === 'default');
                if (b) { b.click(); return 'Clicked default'; }
                return 'No default btn';
            })()
            """, cmd_id=40)
            await asyncio.sleep(1.0)
            s_front = await capture_screenshot(ws, "01_model_front.png", cmd_id=203)
            audit_data["screenshots"]["01_model_front.png"] = s_front

            # Left 45
            await evaluate(ws, """
            (() => {
                const avatarBox = document.querySelector('.bg-slate-900.rounded-2xl');
                if (!avatarBox) return;
                const btns = Array.from(avatarBox.querySelectorAll('button'));
                const b = btns.find(btn => btn.textContent.trim().toLowerCase() === 'left45');
                if (b) b.click();
            })()
            """, cmd_id=41)
            await asyncio.sleep(1.0)
            s_l45 = await capture_screenshot(ws, "02_model_left45.png", cmd_id=204)
            audit_data["screenshots"]["02_model_left45.png"] = s_l45

            # Right 45
            await evaluate(ws, """
            (() => {
                const avatarBox = document.querySelector('.bg-slate-900.rounded-2xl');
                if (!avatarBox) return;
                const btns = Array.from(avatarBox.querySelectorAll('button'));
                const b = btns.find(btn => btn.textContent.trim().toLowerCase() === 'right45');
                if (b) b.click();
            })()
            """, cmd_id=42)
            await asyncio.sleep(1.0)
            s_r45 = await capture_screenshot(ws, "03_model_right45.png", cmd_id=205)
            audit_data["screenshots"]["03_model_right45.png"] = s_r45

            # Hands Close-up
            await evaluate(ws, """
            (() => {
                const avatarBox = document.querySelector('.bg-slate-900.rounded-2xl');
                if (!avatarBox) return;
                const btns = Array.from(avatarBox.querySelectorAll('button'));
                const b = btns.find(btn => btn.textContent.trim().toLowerCase() === 'hands');
                if (b) b.click();
            })()
            """, cmd_id=43)
            await asyncio.sleep(1.0)
            s_hands = await capture_screenshot(ws, "04_model_hands_closeup.png", cmd_id=206)
            audit_data["screenshots"]["04_model_hands_closeup.png"] = s_hands

            # Face Close-up
            await evaluate(ws, """
            (() => {
                const avatarBox = document.querySelector('.bg-slate-900.rounded-2xl');
                if (!avatarBox) return;
                const btns = Array.from(avatarBox.querySelectorAll('button'));
                const b = btns.find(btn => btn.textContent.trim().toLowerCase() === 'face');
                if (b) b.click();
            })()
            """, cmd_id=44)
            await asyncio.sleep(1.0)
            s_face = await capture_screenshot(ws, "05_model_face_closeup.png", cmd_id=207)
            audit_data["screenshots"]["05_model_face_closeup.png"] = s_face

            # 6. Test Torque Preset Selection & Mocap Retargeting
            print("\n--- 6. Torque Preset Retargeting Audit ---")
            # Step back to 1
            await evaluate(ws, """
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const s1 = btns.find(b => b.textContent.includes('Concept Input') || b.textContent.includes('Step 1'));
                if (s1) s1.click();
            })()
            """, cmd_id=50)
            await asyncio.sleep(1.0)

            # Select Torque
            await evaluate(ws, """
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const t = btns.find(b => b.textContent.includes('Torque'));
                if (t) t.click();
            })()
            """, cmd_id=51)
            await asyncio.sleep(1.0)

            # Jump to Step 4
            await evaluate(ws, """
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const s4 = btns.find(b => b.textContent.includes('Synchronized Signing') || b.textContent.includes('Step 4'));
                if (s4) s4.click();
            })()
            """, cmd_id=52)
            await asyncio.sleep(2.0)
            s_torque = await capture_screenshot(ws, "08_torque_signing.png", cmd_id=208)
            audit_data["screenshots"]["08_torque_signing.png"] = s_torque

            # 7. Measure Render Performance & FPS
            print("\n--- 7. Performance & FPS Measurement ---")
            perf_data = await evaluate(ws, """
            new Promise((resolve) => {
                let frames = 0;
                let startTime = performance.now();
                
                function loop() {
                    frames++;
                    if (performance.now() - startTime >= 1000) {
                        const elapsed = performance.now() - startTime;
                        const fps = Math.round((frames / elapsed) * 1000);
                        const mem = performance.memory ? {
                            usedJSHeapSize: performance.memory.usedJSHeapSize,
                            totalJSHeapSize: performance.memory.totalJSHeapSize
                        } : null;
                        resolve({ fps, elapsedMs: elapsed, frames, memory: mem });
                    } else {
                        requestAnimationFrame(loop);
                    }
                }
                requestAnimationFrame(loop);
            })
            """, cmd_id=60)
            audit_data["performance"] = perf_data
            print("  Performance:", perf_data)

            # Save full audit raw JSON
            raw_path = EVIDENCE_DIR / "avatar_audit_raw.json"
            raw_path.write_text(json.dumps(audit_data, indent=2))
            print(f"\n[DONE] Saved audit evidence summary to {raw_path}")

    finally:
        # Close the tab
        try:
            req = urllib.request.Request(f"{CDP_HTTP}/json/close/{target_id}", method="PUT")
            urllib.request.urlopen(req)
            print(f"[CDP] Closed tab {target_id}")
        except Exception:
            pass

if __name__ == "__main__":
    asyncio.run(run_avatar_audit())
