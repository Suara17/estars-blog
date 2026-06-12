<script lang="ts">
  import { onMount } from "svelte";

  interface Props {
    passwordHash: string;
  }

  let { passwordHash }: Props = $props();

  let inputVal = $state("");
  let error = $state(false);
  let visible = $state(false);

  async function sha256(text: string): Promise<string> {
    const data = new TextEncoder().encode(text);
    const hash = await crypto.subtle.digest("SHA-256", data);
    return Array.from(new Uint8Array(hash))
      .map((b) => b.toString(16).padStart(2, "0"))
      .join("");
  }

  async function handleSubmit() {
    const hash = await sha256(inputVal.trim());
    if (hash === passwordHash) {
      sessionStorage.setItem("site-auth", passwordHash);
      visible = false;
      document.body.style.overflow = "";
    } else {
      error = true;
      setTimeout(() => (error = false), 2000);
    }
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === "Enter") handleSubmit();
  }

  onMount(() => {
    const cached = sessionStorage.getItem("site-auth");
    if (cached === passwordHash) {
      visible = false;
    } else {
      visible = true;
      document.body.style.overflow = "hidden";
    }
  });
</script>

{#if visible}
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div class="gate-overlay" onkeydown={handleKeydown}>
    <div class="gate-card">
      <div class="gate-icon">🔒</div>
      <h2 class="gate-title">站点已加密</h2>
      <p class="gate-desc">请输入访问密码以继续浏览</p>
      <input
        class="gate-input"
        class:gate-input-error={error}
        type="password"
        placeholder="输入密码…"
        bind:value={inputVal}
        autofocus
      />
      {#if error}
        <p class="gate-error-msg">密码错误，请重试</p>
      {/if}
      <button class="gate-btn" onclick={handleSubmit}>进入站点</button>
    </div>
  </div>
{/if}

<style>
  .gate-overlay {
    position: fixed;
    inset: 0;
    z-index: 99999;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.85);
    backdrop-filter: blur(12px);
    animation: fadeIn 0.3s ease-out;
  }

  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  .gate-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2.5rem 2rem;
    border-radius: 1rem;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(20px);
    max-width: 360px;
    width: 90%;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    animation: slideUp 0.4s ease-out;
  }

  @keyframes slideUp {
    from { transform: translateY(20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
  }

  .gate-icon {
    font-size: 2.5rem;
    margin-bottom: 0.75rem;
  }

  .gate-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #fff;
    margin: 0 0 0.5rem 0;
  }

  .gate-desc {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.55);
    margin: 0 0 1.25rem 0;
  }

  .gate-input {
    width: 100%;
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;
    border: 1.5px solid rgba(255, 255, 255, 0.15);
    background: rgba(255, 255, 255, 0.08);
    color: #fff;
    font-size: 0.95rem;
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
    box-sizing: border-box;
  }

  .gate-input:focus {
    border-color: var(--primary, #6366f1);
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25);
  }

  .gate-input::placeholder {
    color: rgba(255, 255, 255, 0.3);
  }

  .gate-input-error {
    border-color: #ef4444 !important;
    box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.25) !important;
    animation: shake 0.3s ease-in-out;
  }

  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-6px); }
    75% { transform: translateX(6px); }
  }

  .gate-error-msg {
    font-size: 0.8rem;
    color: #ef4444;
    margin: 0.5rem 0 0 0;
  }

  .gate-btn {
    margin-top: 1rem;
    width: 100%;
    padding: 0.7rem 1rem;
    border-radius: 0.5rem;
    border: none;
    background: var(--primary, #6366f1);
    color: #fff;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s, transform 0.1s;
  }

  .gate-btn:hover {
    filter: brightness(1.1);
  }

  .gate-btn:active {
    transform: scale(0.98);
  }
</style>
