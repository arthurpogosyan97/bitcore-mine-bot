const tg = window.Telegram?.WebApp;
const initData = tg?.initData || "";

const $ = (selector) => document.querySelector(selector);
const elements = {
  loader: $("#loader"),
  loaderText: $("#loaderText"),
  languagePicker: $(".language-picker"),
  langToggle: $("#langToggle"),
  langMenu: $("#langMenu"),
  currentLangFlag: $("#currentLangFlag"),
  tier: $("#tier"),
  profileName: $("#profileName"),
  profileFullName: $("#profileFullName"),
  profileTier: $("#profileTier"),
  profileCoins: $("#profileCoins"),
  profileEarned: $("#profileEarned"),
  profileEnergy: $("#profileEnergy"),
  profileStorage: $("#profileStorage"),
  profileTapLevel: $("#profileTapLevel"),
  profileTapPower: $("#profileTapPower"),
  profileProgressText: $("#profileProgressText"),
  profileProgressBar: $("#profileProgressBar"),
  tapLevel: $("#tapLevel"),
  coins: $("#coins"),
  storageText: $("#storageText"),
  storageBar: $("#storageBar"),
  rate: $("#rate"),
  energy: $("#energy"),
  energyText: $("#energyText"),
  energyBar: $("#energyBar"),
  rank: $("#rank"),
  playerName: $("#playerName"),
  upgrades: $("#upgrades"),
  leaderboard: $("#leaderboard"),
  top100List: $("#top100List"),
  questsList: $("#questsList"),
  achievementsList: $("#achievementsList"),
  boostersList: $("#boostersList"),
  skinsList: $("#skinsList"),
  dailyStreak: $("#dailyStreak"),
  openChestBtn: $("#openChestBtn"),
  currentTeam: $("#currentTeam"),
  toast: $("#toast"),
  collectBtn: $("#collectBtn"),
  dailyBtn: $("#dailyBtn"),
  buyEnergyBtn: $("#buyEnergyBtn"),
  devEnergyBtn: $("#devEnergyBtn"),
  energyPaymentStep: $("#energyPaymentStep"),
  selectedEnergyPack: $("#selectedEnergyPack"),
  devUpgradeBtn: $("#devUpgradeBtn"),
  upgradePaymentStep: $("#upgradePaymentStep"),
  selectedUpgradeText: $("#selectedUpgradeText"),
  tapCoin: $("#tapCoin"),
  tapFx: $("#tapFx"),
  rainField: $("#rainField"),
  collector: $("#collector"),
  dropBtn: $("#dropBtn"),
  rainScore: $("#rainScore"),
  wheelFace: $("#wheelFace"),
  wheelResult: $("#wheelResult"),
  spinWheel: $("#spinWheel"),
  launchStage: $("#launchStage"),
  launchCore: $("#launchCore"),
  launchMultiplier: $("#launchMultiplier"),
  launchStatus: $("#launchStatus"),
  launchHistory: $("#launchHistory"),
  startLaunch: $("#startLaunch"),
  cashoutLaunch: $("#cashoutLaunch"),
  refLink: $("#refLink"),
  copyRefBtn: $("#copyRefBtn"),
};

const languages = {
  en: { flag: "/static/flags/en.svg", name: "English" },
  ru: { flag: "/static/flags/ru.svg", name: "Русский" },
  kk: { flag: "/static/flags/kk.svg", name: "Қазақша" },
  uz: { flag: "/static/flags/uz.svg", name: "O'zbekcha" },
  az: { flag: "/static/flags/az.svg", name: "Azərbaycanca" },
  hy: { flag: "/static/flags/hy.svg", name: "Հայերեն" },
  ka: { flag: "/static/flags/ka.svg", name: "ქართული" },
  ky: { flag: "/static/flags/ky.svg", name: "Кыргызча" },
  tg: { flag: "/static/flags/tg.svg", name: "Тоҷикӣ" },
  be: { flag: "/static/flags/be.svg", name: "Беларуская" },
};

const translations = {
  en: {
    brand: "BitCore Mine",
    language: "Language",
    coins: "coins",
    storage: "Storage",
    miningRate: "Mining Rate",
    energy: "Energy",
    rank: "Rank",
    collect: "Collect",
    collectCoins: "Collect Coins",
    dailyDrop: "Daily Drop",
    buyEnergy: "Buy Energy",
    profile: "Profile",
    openProfile: "Open Profile",
    player: "Player",
    status: "Status",
    tapLevel: "Tap Level",
    tapPower: "Tap Power",
    levelProgress: "Level Progress",
    playEarn: "Play & Earn",
    miniGames: "Mini games",
    coreCatch: "Core Catch",
    wheel: "Reactor Wheel",
    coreLaunch: "Core Launch",
    tapHint: "Tap the BitCore coin to collect quick bits.",
    dropCopy: "Move the collector and catch falling BitCore coins.",
    startDrop: "Start Drop",
    spinWheel: "Spin Reactor",
    startLaunch: "Launch Core",
    cashoutLaunch: "Cash Out",
    launchReady: "Choose a bet and launch the core",
    launchCopy: "Cash out before the BitCore reactor overheats.",
    launchRunning: "Reactor is heating",
    launchCrashed: "Core overheated",
    launchCashed: "Core secured",
    autoOff: "Auto: Off",
    wheelReady: "Choose a bet and fire the reactor",
    wheelRisk: "Land on a charged sector before the core cools.",
    won: "You won",
    missed: "Missed. Try again",
    jackpot: "Jackpot",
    upgradeRig: "Upgrade Rig",
    quests: "Quests",
    rewards: "Rewards",
    skins: "Skins",
    team: "Team",
    questsCopy: "Complete daily goals and claim extra coins.",
    achievements: "Achievements",
    dailyStreak: "Daily streak",
    openChest: "Open Chest",
    chestCopy: "Chest costs 75 coins and can drop coins, energy, or a booster.",
    skinsCopy: "Collect BitCore coin skins and choose your active core.",
    currentTeam: "Current team",
    teamCopy: "Teams are the base for future clan rankings and shared bonuses.",
    claimReward: "Claim",
    claimed: "Claimed",
    buy: "Buy",
    select: "Select",
    selected: "Selected",
    leaderboard: "Leaderboard",
    ratingTop: "Top 100 Players",
    earnedTotal: "Total Earned",
    upgradeCopy: "Improve your rig to mine faster, store more, and build tap power.",
    topMiners: "Top miners",
    loading: "Igniting the core...",
    caught: "Caught",
    storageFull: "Storage is full. Collect coins first.",
    noEnergy: "Energy is empty. Buy energy or wait.",
    refTitle: "Invite miners",
    refCopy: "Share your referral link. You get 500 coins for every invited friend who starts the bot.",
    copyRef: "Copy Link",
    copied: "Copied",
    tapLevelHow: "How tap level grows",
    tapLevelRule: "Every coin earned by tapping counts toward tap progress. Higher levels increase coins per tap.",
    energyPayCopy: "Choose how you want to refill energy. Payments will be connected later.",
    telegramStars: "Telegram Stars",
    telegramStarsCopy: "Fast in-app top-up",
    tonWallet: "TON Wallet",
    tonWalletCopy: "Top up via TON wallet",
    tariffStarter: "Starter Charge",
    tariffWorker: "Worker Battery",
    tariffReactor: "Reactor Pack",
    tariffQuantum: "Quantum Cell",
    tariffUnlimited: "Overdrive Tank",
    paymentsSoon: "Payments will be connected later",
    selectTariffFirst: "Select a tariff first",
    selectUpgradeFirst: "Select an upgrade first",
    testEnergy: "Test refill for coins",
    testUpgrade: "Test upgrade for coins",
    claim: "Claim",
    dailyClaimCopy: "Your daily core bonus is ready.",
    upgrade_drill_title: "Plasma Drill",
    upgrade_drill_desc: "Increases passive coin mining.",
    upgrade_generator_title: "Bit Reactor",
    upgrade_generator_desc: "Boosts mine power and energy capacity.",
    upgrade_storage_title: "Core Vault",
    upgrade_storage_desc: "Increases maximum storage.",
  },
  ru: {
    brand: "BitCore Mine",
    language: "Язык",
    coins: "монеты",
    storage: "Хранилище",
    miningRate: "Добыча",
    energy: "Энергия",
    rank: "Ранг",
    collect: "Собрать",
    collectCoins: "Собрать монеты",
    dailyDrop: "Дневной бонус",
    buyEnergy: "Купить энергию",
    profile: "Профиль",
    openProfile: "Открыть профиль",
    player: "Игрок",
    status: "Статус",
    tapLevel: "Уровень тапа",
    tapPower: "Сила тапа",
    levelProgress: "Прогресс уровня",
    playEarn: "Играй и добывай",
    miniGames: "Мини-игры",
    coreCatch: "Ловец ядра",
    wheel: "Колесо реактора",
    coreLaunch: "Запуск ядра",
    tapHint: "Тапай по монете BitCore, чтобы быстро собирать монеты.",
    dropCopy: "Двигай ловушку и собирай падающие монетки BitCore.",
    startDrop: "Запустить дроп",
    spinWheel: "Запустить реактор",
    startLaunch: "Запустить ядро",
    cashoutLaunch: "Забрать",
    launchReady: "Выбери ставку и запусти ядро",
    launchCopy: "Забери монеты до перегрева реактора BitCore.",
    launchRunning: "Реактор нагревается",
    launchCrashed: "Ядро перегрелось",
    launchCashed: "Ядро сохранено",
    autoOff: "Авто: выкл",
    wheelReady: "Выбери ставку и запусти реактор",
    wheelRisk: "Попади на заряженный сектор, пока ядро не остыло.",
    won: "Ты выиграл",
    missed: "Мимо. Попробуй еще",
    jackpot: "Джекпот",
    upgradeRig: "Улучшения",
    quests: "Квесты",
    rewards: "Награды",
    skins: "Скины",
    team: "Команда",
    questsCopy: "Выполняй ежедневные цели и забирай дополнительные монеты.",
    achievements: "Достижения",
    dailyStreak: "Серия входов",
    openChest: "Открыть сундук",
    chestCopy: "Сундук стоит 75 монет и может дать монеты, энергию или бустер.",
    skinsCopy: "Собирай скины монеты BitCore и выбирай активное ядро.",
    currentTeam: "Текущая команда",
    teamCopy: "Команды станут основой для будущего рейтинга кланов и общих бонусов.",
    claimReward: "Забрать",
    claimed: "Забрано",
    buy: "Купить",
    select: "Выбрать",
    selected: "Выбрано",
    leaderboard: "Рейтинг",
    ratingTop: "Топ-100 игроков",
    earnedTotal: "Всего заработано",
    upgradeCopy: "Улучшай установку, чтобы быстрее добывать, хранить больше и усиливать тап.",
    topMiners: "Лучшие шахтеры",
    loading: "Запускаем ядро...",
    caught: "Поймано",
    storageFull: "Хранилище заполнено. Сначала собери монеты.",
    noEnergy: "Энергия закончилась. Купи энергию или подожди.",
    refTitle: "Приглашай майнеров",
    refCopy: "Поделись реферальной ссылкой. За каждого приглашенного друга, который запустит бота, ты получишь 500 монет.",
    copyRef: "Копировать ссылку",
    copied: "Скопировано",
    tapLevelHow: "Как растет уровень тапа",
    tapLevelRule: "Каждая монета, добытая тапом, идет в прогресс. Чем выше уровень, тем больше монет за тап.",
    energyPayCopy: "Выбери способ пополнения энергии. Оплату подключим позже.",
    telegramStars: "Telegram Stars",
    telegramStarsCopy: "Быстрое пополнение внутри Telegram",
    tonWallet: "TON Wallet",
    tonWalletCopy: "Пополнение через TON-кошелек",
    tariffStarter: "Стартовый заряд",
    tariffWorker: "Рабочая батарея",
    tariffReactor: "Реакторный пакет",
    tariffQuantum: "Квантовая ячейка",
    tariffUnlimited: "Овердрайв-бак",
    paymentsSoon: "Оплату подключим позже",
    selectTariffFirst: "Сначала выбери тариф",
    selectUpgradeFirst: "Сначала выбери улучшение",
    testEnergy: "Тестовое пополнение за монеты",
    testUpgrade: "Тестовая покупка за монеты",
    claim: "Забрать",
    dailyClaimCopy: "Твой дневной бонус ядра готов.",
    upgrade_drill_title: "Плазменный бур",
    upgrade_drill_desc: "Увеличивает пассивную добычу монет.",
    upgrade_generator_title: "Бит-реактор",
    upgrade_generator_desc: "Усиливает шахту и увеличивает запас энергии.",
    upgrade_storage_title: "Хранилище ядра",
    upgrade_storage_desc: "Увеличивает максимальный объем хранилища.",
  },
};

const fallbackLabels = {
  kk: { language: "Тіл", profile: "Профиль", openProfile: "Профиль ашу", referrals: "Рефералдар", refTitle: "Майнерлерді шақыр", refCopy: "Реферал сілтемеңмен бөліс. Кейін шақырылған ойыншылар бонус әкеледі.", copyRef: "Сілтемені көшіру", collect: "Жинау", startDrop: "Дроп бастау", spinWheel: "Айналдыру" },
  uz: { language: "Til", profile: "Profil", openProfile: "Profilni ochish", referrals: "Referallar", refTitle: "Maynerlarni taklif qiling", refCopy: "Referal havolangizni ulashing. Keyin taklif qilingan o'yinchilar bonus olib keladi.", copyRef: "Havolani nusxalash", collect: "Yig'ish", startDrop: "Drop boshlash", spinWheel: "Aylantirish" },
  az: { language: "Dil", profile: "Profil", openProfile: "Profili aç", referrals: "Referallar", refTitle: "Maynerləri dəvət et", refCopy: "Referal linkini paylaş. Sonra dəvət olunan oyunçular bonus gətirəcək.", copyRef: "Linki kopyala", collect: "Topla", startDrop: "Drop başlat", spinWheel: "Fırlat" },
  hy: { language: "Լեզու", profile: "Պրոֆիլ", openProfile: "Բացել պրոֆիլը", referrals: "Ռեֆերալներ", refTitle: "Հրավիրիր մայներների", refCopy: "Կիսվիր քո հղումով։ Հետո հրավիրված խաղացողները բոնուսներ կբերեն։", copyRef: "Պատճենել հղումը", collect: "Հավաքել", startDrop: "Սկսել", spinWheel: "Պտտել" },
  ka: { language: "ენა", profile: "პროფილი", openProfile: "პროფილის გახსნა", referrals: "რეფერალები", refTitle: "მოიწვიე მაინერები", refCopy: "გააზიარე რეფერალური ბმული. მოგვიანებით მოწვეული მოთამაშეები ბონუსებს მოგიტანენ.", copyRef: "ბმულის კოპირება", collect: "შეგროვება", startDrop: "დაწყება", spinWheel: "დატრიალება" },
  ky: { language: "Тил", profile: "Профиль", openProfile: "Профиль ачуу", referrals: "Рефералдар", refTitle: "Майнерлерди чакыр", refCopy: "Реферал шилтемең менен бөлүш. Кийин чакырылган оюнчулар бонус алып келет.", copyRef: "Шилтемени көчүрүү", collect: "Жыйноо", startDrop: "Дроп баштоо", spinWheel: "Айлантуу" },
  tg: { language: "Забон", profile: "Профил", openProfile: "Кушодани профил", referrals: "Рефералҳо", refTitle: "Майнерҳоро даъват кун", refCopy: "Истиноди рефералии худро фирист. Баъд бозигарони даъватшуда бонус меоранд.", copyRef: "Нусхаи истинод", collect: "Ҷамъ кардан", startDrop: "Оғоз", spinWheel: "Чархондан" },
  be: { language: "Мова", profile: "Профіль", openProfile: "Адкрыць профіль", referrals: "Рэфералы", refTitle: "Запрашай майнераў", refCopy: "Падзяліся рэферальнай спасылкай. Пазней запрошаныя гульцы будуць прыносіць бонусы.", copyRef: "Скапіраваць спасылку", collect: "Сабраць", startDrop: "Пачаць", spinWheel: "Круціць" },
};

const wheelPrizes = [
  { label: "0", note: "MISS", kind: "miss", dark: true },
  { label: "+10", note: "COINS", kind: "coin coin-10" },
  { label: "+20", note: "COINS", kind: "coin coin-20", dark: true },
  { label: "+30", note: "COINS", kind: "coin coin-30" },
  { label: "0", note: "MISS", kind: "miss" },
  { label: "+50", note: "COINS", kind: "coin coin-50" },
  { label: "x2", note: "BET", kind: "multiplier", dark: true },
  { label: "JACKPOT", note: "+500", kind: "jackpot", dark: true },
];

let selectedBet = 50;
let selectedLaunchBet = 10;
let selectedAutoCashout = 0;
let selectedEnergyPack = null;
let selectedUpgradeKey = null;
let dailyShown = false;
let wheelTurns = 0;
let wheelScanTimer = null;
let launchRound = null;
let launchTimer = null;
let launchCashoutPending = false;
let launchHistory = [];
let lastTouchEnd = 0;
let lastTapCoinTouch = 0;
let currentLang = localStorage.getItem("bitcore_lang") || "en";
let audioContext;

if (tg) {
  tg.ready();
  tg.expand();
  tg.setHeaderColor("#090b12");
  tg.setBackgroundColor("#090b12");
}

function t(key) {
  return fallbackLabels[currentLang]?.[key] || translations[currentLang]?.[key] || translations.en[key] || key;
}

function optionalText(key) {
  return fallbackLabels[currentLang]?.[key] || translations[currentLang]?.[key] || translations.en[key] || "";
}

function applyLanguage() {
  document.documentElement.lang = currentLang;
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n);
  });
  elements.currentLangFlag.src = languages[currentLang]?.flag || languages.en.flag;
  elements.currentLangFlag.alt = languages[currentLang]?.name || languages.en.name;
  elements.loaderText.textContent = t("loading");
  document.querySelectorAll(".lang").forEach((button) => {
    button.classList.toggle("active", button.dataset.lang === currentLang);
  });
  elements.rainScore.textContent = `${t("caught")}: 0`;
  if (!launchRound) {
    elements.launchStatus.textContent = t("launchReady");
  }
}

function authHeaders() {
  return initData ? { Authorization: `tma ${initData}` } : {};
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
      ...(options.headers || {}),
    },
  });
  const data = await response.json();
  if (!response.ok && !data.toast) throw new Error(data.message || "Request failed");
  return data;
}

function showToast(message) {
  if (!message) return;
  elements.toast.textContent = message;
  elements.toast.classList.add("show");
  window.setTimeout(() => elements.toast.classList.remove("show"), 1800);
  tg?.HapticFeedback?.notificationOccurred("success");
}

function playTone(kind) {
  try {
    audioContext ||= new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gain = audioContext.createGain();
    oscillator.connect(gain);
    gain.connect(audioContext.destination);
    oscillator.type = kind === "miss" ? "triangle" : "sine";
    oscillator.frequency.value = kind === "miss" ? 180 : kind === "coin" ? 880 : kind === "spin" ? 260 : kind === "jackpot" ? 660 : 440;
    gain.gain.setValueAtTime(0.001, audioContext.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.08, audioContext.currentTime + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.22);
    oscillator.start();
    oscillator.stop(audioContext.currentTime + 0.24);
  } catch {
    // Audio is optional and may be blocked by the client.
  }
}

function playSpinSound() {
  let ticks = 0;
  const timer = window.setInterval(() => {
    playTone("spin");
    ticks += 1;
    if (ticks >= 18) window.clearInterval(timer);
  }, 230);
}

function renderWheel() {
  elements.wheelFace.innerHTML = wheelPrizes
    .map((prize, index) => {
      return `
        <div class="wheel-prize ${prize.kind} ${prize.dark ? "dark" : ""}" data-prize-index="${index}">
          <strong>${prize.label}</strong>
          <span>${prize.note}</span>
        </div>
      `;
    })
    .join("");
}

function clearWheelSelection() {
  window.clearInterval(wheelScanTimer);
  wheelScanTimer = null;
  elements.wheelFace.querySelectorAll(".wheel-prize").forEach((node) => {
    node.classList.remove("scan", "selected");
  });
}

function scanWheelTo(index, result) {
  clearWheelSelection();
  const cells = [...elements.wheelFace.querySelectorAll(".wheel-prize")];
  let step = 0;
  const totalSteps = 28 + index;
  wheelScanTimer = window.setInterval(() => {
    cells.forEach((cell) => cell.classList.remove("scan"));
    cells[step % cells.length]?.classList.add("scan");
    playTone("spin");
    step += 1;
    if (step > totalSteps) {
      window.clearInterval(wheelScanTimer);
      wheelScanTimer = null;
      cells.forEach((cell) => cell.classList.remove("scan"));
      cells[index]?.classList.add("selected");
      setWheelResult(result);
    }
  }, 95);
}

function upgradeTitle(upgrade) {
  return optionalText(`upgrade_${upgrade.key}_title`) || upgrade.title;
}

function upgradeDescription(upgrade) {
  return optionalText(`upgrade_${upgrade.key}_desc`) || upgrade.description;
}

function wheelMessage(result) {
  if (result.kind === "miss") {
    return { title: t("missed"), detail: `-${result.bet}`, tone: "miss" };
  }
  if (result.kind === "jackpot") {
    return { title: `${t("jackpot")} +${result.winnings}`, detail: "BitCore Mine", tone: "jackpot" };
  }
  return { title: `${t("won")} +${result.winnings}`, detail: result.label, tone: "win" };
}

function setWheelResult(result) {
  const message = wheelMessage(result);
  elements.wheelResult.className = `wheel-result ${message.tone}`;
  elements.wheelResult.innerHTML = `<strong>${message.title}</strong><span>${message.detail}</span>`;
  elements.wheelFace.classList.remove("is-spinning");
  elements.wheelFace.classList.toggle("win-glow", result.kind !== "miss");

  if (result.kind === "miss") {
    playTone("miss");
    tg?.HapticFeedback?.notificationOccurred("warning");
  } else if (result.kind === "jackpot") {
    playTone("jackpot");
    tg?.HapticFeedback?.notificationOccurred("success");
    tg?.HapticFeedback?.impactOccurred("heavy");
  } else {
    playTone("win");
    tg?.HapticFeedback?.notificationOccurred("success");
  }
}

function renderFeatureList(node, items, action, buttonLabel = t("claimReward")) {
  if (!node) return;
  node.innerHTML = items
    .map((item) => {
      const progress = item.target ? `<span>${item.current}/${item.target}</span>` : "";
      const disabled = item.claimed || (item.done === false);
      const label = item.claimed ? t("claimed") : buttonLabel;
      return `
        <article class="feature-item">
          <div>
            <strong>${item.title}</strong>
            <p>${item.description || ""}</p>
            ${progress}
          </div>
          <button data-${action}="${item.key}" ${disabled ? "disabled" : ""}>${label}</button>
        </article>
      `;
    })
    .join("");
}

function render(state) {
  const player = state.player;
  elements.tier.textContent = player.tier;
  elements.profileName.textContent = player.username ? `@${player.username}` : player.name;
  elements.tapLevel.textContent = `Lv.${player.tap.level} ${player.tap.title}`;
  elements.profileFullName.textContent = player.username ? `@${player.username}` : player.name;
  elements.profileTier.textContent = player.tier;
  elements.profileCoins.textContent = player.coins.toLocaleString();
  elements.profileEarned.textContent = player.earnedTotal.toLocaleString();
  elements.profileEnergy.textContent = `${player.energy}/${player.energyCap}`;
  elements.profileStorage.textContent = `${player.pending}/${player.capacity}`;
  elements.profileTapLevel.textContent = `Lv.${player.tap.level} ${player.tap.title}`;
  elements.profileTapPower.textContent = `+${player.tap.tapPower}`;
  elements.profileProgressText.textContent = `${player.tap.progress}%`;
  elements.profileProgressBar.style.width = `${player.tap.progress}%`;
  if (elements.dailyStreak) elements.dailyStreak.textContent = `${player.dailyStreak || 0}`;
  if (elements.currentTeam) elements.currentTeam.textContent = player.team || "-";
  elements.coins.textContent = player.coins.toLocaleString();
  elements.storageText.textContent = `${player.pending}/${player.capacity}`;
  elements.storageBar.style.width = `${Math.min(player.storagePercent, 100)}%`;
  elements.rate.textContent = `${player.rate}/h`;
  elements.energy.textContent = player.energy;
  elements.energyText.textContent = `${player.energy}/${player.energyCap}`;
  elements.energyBar.style.width = `${Math.round((player.energy / player.energyCap) * 100)}%`;
  elements.buyEnergyBtn.classList.toggle("energy-buy-hidden", player.energy > 0);
  elements.buyEnergyBtn.classList.toggle("energy-buy-visible", player.energy <= 0);
  if (player.dailyAvailable && !dailyShown) {
    dailyShown = true;
    window.setTimeout(() => openModal("dailyModal"), 500);
  }
  if (elements.playerName) elements.playerName.textContent = player.name;
  elements.refLink.textContent = player.referralLink;

  const selfRank = state.leaderboard.find((row) => row.name === player.name);
  elements.rank.textContent = selfRank ? `#${selfRank.rank}` : "-";

  elements.upgrades.innerHTML = state.upgrades
    .map(
      (upgrade) => `
        <article class="upgrade">
          <div>
            <strong>${upgrade.icon} ${upgradeTitle(upgrade)} Lv.${upgrade.level}</strong>
            <p>${upgradeDescription(upgrade)}</p>
          </div>
          <button data-select-upgrade="${upgrade.key}" data-upgrade-cost="${upgrade.cost}">${upgrade.cost}</button>
        </article>
      `,
    )
    .join("");

  if (elements.leaderboard) {
    elements.leaderboard.innerHTML = state.leaderboard
      .map(
        (row) => `
          <div class="leader-row">
            <strong>#${row.rank}</strong>
            <span>${row.name}</span>
            <strong>${row.coins}</strong>
          </div>
        `,
      )
      .join("");
  }

  if (state.roulette) {
    wheelTurns += 1;
    scanWheelTo(state.roulette.index, state.roulette);
  }

  renderFeatureList(elements.questsList, state.quests || [], "quest");
  renderFeatureList(elements.achievementsList, state.achievements || [], "achievement");
  if (elements.boostersList) {
    elements.boostersList.innerHTML = (state.boosters || [])
      .map((booster) => `
        <article class="feature-item">
          <div>
            <strong>${booster.title}</strong>
            <p>${booster.description}</p>
            <span>${booster.cost} ${t("coins")}</span>
          </div>
          <button data-booster="${booster.key}">${t("buy")}</button>
        </article>
      `)
      .join("");
  }
  if (elements.skinsList) {
    elements.skinsList.innerHTML = (state.skins || [])
      .map((skin) => `
        <article class="feature-item skin-item ${skin.selected ? "active" : ""}">
          <div>
            <strong>${skin.title}</strong>
            <p>${skin.owned ? t("select") : `${skin.cost} ${t("coins")}`}</p>
          </div>
          <button data-skin="${skin.key}" ${skin.selected ? "disabled" : ""}>${skin.selected ? t("selected") : skin.owned ? t("select") : t("buy")}</button>
        </article>
      `)
      .join("");
  }

  if (state.tap?.status === "no_energy") {
    showToast(t("noEnergy"));
    return;
  }
  if (state.tap?.status === "storage_full") {
    showToast(t("storageFull"));
    return;
  }

  showToast(state.toast);
}

async function loadTop100() {
  const data = await api("/api/leaderboard");
  elements.top100List.innerHTML = data.players
    .map(
      (row) => `
        <div class="top100-row">
          <strong>#${row.rank}</strong>
          <span>${row.name}</span>
          <strong>${row.coins.toLocaleString()}</strong>
        </div>
      `,
    )
    .join("");
}

function openModal(id) {
  document.getElementById(id)?.classList.add("open");
  if (id === "ratingModal") loadTop100();
}

function closeModals() {
  document.querySelectorAll(".modal.open").forEach((modal) => modal.classList.remove("open"));
}

async function refresh() {
  render(await api("/api/state"));
}

async function runAction(button, action) {
  button.disabled = true;
  try {
    render(await action());
  } catch (error) {
    showToast(error.message);
    tg?.HapticFeedback?.notificationOccurred("error");
  } finally {
    button.disabled = false;
  }
}

function tapEffect() {
  elements.tapCoin.classList.remove("tap-hit");
  elements.tapFx.classList.remove("flash");
  void elements.tapCoin.offsetWidth;
  elements.tapCoin.classList.add("tap-hit");
  elements.tapFx.classList.add("flash");

  const float = document.createElement("span");
  float.className = "tap-float";
  float.textContent = "+1";
  float.style.left = `${48 + Math.random() * 38}%`;
  float.style.top = `${42 + Math.random() * 20}%`;
  elements.tapCoin.parentElement.appendChild(float);
  window.setTimeout(() => float.remove(), 820);
}

function startDropGame() {
  let caught = 0;
  let collectorX = elements.rainField.clientWidth / 2 - 58;
  const coins = [];

  function setCollector(x) {
    collectorX = Math.max(0, Math.min(x, elements.rainField.clientWidth - 116));
    elements.collector.style.left = `${collectorX}px`;
  }

  function moveCollector(clientX) {
    const rect = elements.rainField.getBoundingClientRect();
    setCollector(clientX - rect.left - 58);
  }

  elements.rainField.onpointermove = (event) => moveCollector(event.clientX);
  elements.rainField.onpointerdown = (event) => moveCollector(event.clientX);
  elements.dropBtn.disabled = true;
  elements.rainScore.textContent = `${t("caught")}: 0`;

  const spawn = window.setInterval(() => {
    const coin = document.createElement("div");
    coin.className = "falling-coin";
    coin.innerHTML = '<img src="/assets/bitcore-coin.png" alt="">';
    coin.style.left = `${Math.random() * (elements.rainField.clientWidth - 38)}px`;
    elements.rainField.appendChild(coin);
    coins.push({ node: coin, y: -40, speed: 2.7 + Math.random() * 2.8 });
  }, 260);

  const loop = window.setInterval(() => {
    for (let index = coins.length - 1; index >= 0; index -= 1) {
      const coin = coins[index];
      coin.y += coin.speed;
      coin.node.style.top = `${coin.y}px`;
      const coinX = parseFloat(coin.node.style.left);
      const hitY = coin.y > elements.rainField.clientHeight - 52;
      const hitX = coinX + 38 > collectorX && coinX < collectorX + 116;
      if (hitY && hitX) {
        caught += 1;
        playTone("coin");
        tg?.HapticFeedback?.impactOccurred("light");
        elements.rainScore.textContent = `${t("caught")}: ${caught}`;
        coin.node.remove();
        coins.splice(index, 1);
      } else if (coin.y > elements.rainField.clientHeight) {
        coin.node.remove();
        coins.splice(index, 1);
      }
    }
  }, 16);

  window.setTimeout(async () => {
    window.clearInterval(spawn);
    window.clearInterval(loop);
    coins.forEach((coin) => coin.node.remove());
    elements.rainField.onpointermove = null;
    elements.rainField.onpointerdown = null;
    elements.dropBtn.disabled = false;
    render(await api("/api/falling/reward", {
      method: "POST",
      body: JSON.stringify({ caught }),
    }));
  }, 12000);
}

function randomBetween(min, max) {
  return Math.round(min + Math.random() * (max - min));
}

function configureLaunchFlight() {
  const direction = Math.random() > 0.5 ? 1 : -1;
  const tilt = direction * randomBetween(8, 18);
  const points = [
    ["--flight-x1", direction * randomBetween(18, 52)],
    ["--flight-y1", -randomBetween(32, 72)],
    ["--flight-x2", direction * -randomBetween(22, 66)],
    ["--flight-y2", -randomBetween(78, 128)],
    ["--flight-x3", direction * randomBetween(8, 44)],
    ["--flight-y3", -randomBetween(118, 174)],
  ];
  points.forEach(([name, value]) => elements.launchStage.style.setProperty(name, `${value}px`));
  elements.launchStage.style.setProperty("--flight-tilt-a", `${Math.round(tilt * -0.45)}deg`);
  elements.launchStage.style.setProperty("--flight-tilt-b", `${tilt}deg`);
  elements.launchStage.style.setProperty("--flight-tilt-c", `${Math.round(tilt * -0.75)}deg`);
  elements.launchStage.style.setProperty("--flight-duration", `${randomBetween(1050, 1550)}ms`);
}

function renderLaunchHistory() {
  elements.launchHistory.innerHTML = launchHistory
    .map((item) => `<span class="${item.status}">x${item.multiplier.toFixed(2)}</span>`)
    .join("");
}

function setLaunchIdle(message = t("launchReady")) {
  window.clearInterval(launchTimer);
  launchTimer = null;
  launchRound = null;
  launchCashoutPending = false;
  elements.launchStage.classList.remove("running", "crashed", "cashed");
  elements.launchMultiplier.textContent = "x1.00";
  elements.launchStatus.textContent = message;
  elements.startLaunch.disabled = false;
  elements.cashoutLaunch.disabled = true;
}

function setLaunchResult(result) {
  window.clearInterval(launchTimer);
  launchTimer = null;
  launchRound = null;
  launchCashoutPending = false;
  elements.launchStage.classList.remove("running", "crashed", "cashed");
  elements.launchStage.classList.add(result.status === "cashed" ? "cashed" : "crashed");
  const multiplier = Number(result.multiplier || 1);
  elements.launchMultiplier.textContent = `x${multiplier.toFixed(2)}`;
  elements.launchStatus.textContent = result.status === "cashed"
    ? `${t("launchCashed")} +${result.winnings}`
    : t("launchCrashed");
  launchHistory = [{ status: result.status, multiplier }, ...launchHistory].slice(0, 8);
  renderLaunchHistory();
  elements.startLaunch.disabled = false;
  elements.cashoutLaunch.disabled = true;
  playTone(result.status === "cashed" ? "jackpot" : "miss");
  tg?.HapticFeedback?.notificationOccurred(result.status === "cashed" ? "success" : "warning");
}

async function startCoreLaunch() {
  if (launchRound) return;
  configureLaunchFlight();
  launchCashoutPending = false;
  elements.startLaunch.disabled = true;
  elements.cashoutLaunch.disabled = false;
  elements.launchStage.classList.remove("crashed", "cashed");
  elements.launchStage.classList.add("running");
  elements.launchStatus.textContent = t("launchRunning");
  elements.launchMultiplier.textContent = "x1.00";
  playTone("spin");

  try {
    const state = await api("/api/core-launch/start", {
      method: "POST",
      body: JSON.stringify({ bet: selectedLaunchBet }),
    });
    render(state);
    if (!state.launch) {
      setLaunchIdle();
      return;
    }
    launchRound = {
      id: state.launch.roundId,
      startedAt: performance.now(),
      growth: state.launch.growth,
      crashAfterMs: state.launch.crashAfterMs,
    };
    elements.startLaunch.disabled = true;
    elements.cashoutLaunch.disabled = false;
    elements.launchStage.classList.add("running");
    launchTimer = window.setInterval(() => {
      const elapsedMs = performance.now() - launchRound.startedAt;
      const multiplier = 1 + (elapsedMs / 1000) * launchRound.growth;
      elements.launchMultiplier.textContent = `x${multiplier.toFixed(2)}`;
      if (selectedAutoCashout && multiplier >= selectedAutoCashout && !launchCashoutPending) {
        cashoutCoreLaunch();
        return;
      }
      if (elapsedMs >= launchRound.crashAfterMs) {
        cashoutCoreLaunch();
      }
    }, 50);
  } catch (error) {
    setLaunchIdle();
    showToast(error.message);
  }
}

async function cashoutCoreLaunch() {
  if (!launchRound || launchCashoutPending) return;
  launchCashoutPending = true;
  const roundId = launchRound.id;
  elements.cashoutLaunch.disabled = true;
  try {
    const state = await api("/api/core-launch/cashout", {
      method: "POST",
      body: JSON.stringify({ roundId }),
    });
    if (!state.launchResult) {
      setLaunchIdle();
      render(state);
      return;
    }
    setLaunchResult(state.launchResult);
    render(state);
  } catch (error) {
    setLaunchIdle(t("launchCrashed"));
    showToast(error.message);
  }
}

elements.langToggle.addEventListener("click", () => {
  elements.languagePicker.classList.toggle("open");
});

document.addEventListener("click", (event) => {
  if (!elements.languagePicker.contains(event.target)) {
    elements.languagePicker.classList.remove("open");
  }
});

document.querySelectorAll(".lang").forEach((button) => {
  button.addEventListener("click", () => {
    currentLang = button.dataset.lang;
    localStorage.setItem("bitcore_lang", currentLang);
    elements.languagePicker.classList.remove("open");
    applyLanguage();
  });
});

elements.collectBtn.addEventListener("click", () => {
  runAction(elements.collectBtn, () => api("/api/collect", { method: "POST", body: "{}" }));
});

elements.dailyBtn.addEventListener("click", () => {
  runAction(elements.dailyBtn, async () => {
    const state = await api("/api/daily", { method: "POST", body: "{}" });
    closeModals();
    return state;
  });
});

elements.questsList.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-quest]");
  if (!button) return;
  runAction(button, () => api("/api/quest/claim", {
    method: "POST",
    body: JSON.stringify({ key: button.dataset.quest }),
  }));
});

elements.achievementsList.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-achievement]");
  if (!button) return;
  runAction(button, () => api("/api/achievement/claim", {
    method: "POST",
    body: JSON.stringify({ key: button.dataset.achievement }),
  }));
});

elements.openChestBtn.addEventListener("click", () => {
  runAction(elements.openChestBtn, () => api("/api/chest/open", { method: "POST", body: "{}" }));
});

elements.boostersList.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-booster]");
  if (!button) return;
  runAction(button, () => api("/api/booster/buy", {
    method: "POST",
    body: JSON.stringify({ key: button.dataset.booster }),
  }));
});

elements.skinsList.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-skin]");
  if (!button) return;
  runAction(button, () => api("/api/skin/buy", {
    method: "POST",
    body: JSON.stringify({ key: button.dataset.skin }),
  }));
});

document.querySelectorAll("[data-team-name]").forEach((button) => {
  button.addEventListener("click", () => {
    runAction(button, () => api("/api/team/join", {
      method: "POST",
      body: JSON.stringify({ name: button.dataset.teamName }),
    }));
  });
});

document.querySelectorAll("[data-energy-pack]").forEach((button) => {
  button.addEventListener("click", () => {
    selectedEnergyPack = button.dataset.energyPack;
    document.querySelectorAll("[data-energy-pack]").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    elements.selectedEnergyPack.textContent = button.innerText.replace(/\s+/g, " ").trim();
    elements.energyPaymentStep.classList.add("open");
  });
});

document.querySelectorAll("[data-energy-pay]").forEach((button) => {
  button.addEventListener("click", () => {
    if (!selectedEnergyPack) {
      showToast(t("selectTariffFirst"));
      return;
    }
    showToast(t("paymentsSoon"));
  });
});

elements.devEnergyBtn.addEventListener("click", () => {
  if (!selectedEnergyPack) {
    showToast(t("selectTariffFirst"));
    return;
  }
  runAction(elements.devEnergyBtn, async () => {
    const state = await api("/api/energy/buy", {
      method: "POST",
      body: JSON.stringify({ pack: selectedEnergyPack }),
    });
    selectedEnergyPack = null;
    elements.energyPaymentStep.classList.remove("open");
    closeModals();
    return state;
  });
});

elements.upgrades.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-select-upgrade]");
  if (!button) return;
  selectedUpgradeKey = button.dataset.selectUpgrade;
  elements.upgrades.querySelectorAll("[data-select-upgrade]").forEach((item) => item.classList.remove("active"));
  button.classList.add("active");
  elements.selectedUpgradeText.textContent = `${button.closest(".upgrade").querySelector("strong").textContent} · ${button.dataset.upgradeCost} ${t("coins")}`;
  elements.upgradePaymentStep.classList.add("open");
});

document.querySelectorAll("[data-upgrade-pay]").forEach((button) => {
  button.addEventListener("click", () => {
    if (!selectedUpgradeKey) {
      showToast(t("selectUpgradeFirst"));
      return;
    }
    showToast(t("paymentsSoon"));
  });
});

elements.devUpgradeBtn.addEventListener("click", () => {
  if (!selectedUpgradeKey) {
    showToast(t("selectUpgradeFirst"));
    return;
  }
  runAction(elements.devUpgradeBtn, async () => {
    const state = await api("/api/upgrade", {
      method: "POST",
      body: JSON.stringify({ key: selectedUpgradeKey }),
    });
    selectedUpgradeKey = null;
    elements.upgradePaymentStep.classList.remove("open");
    closeModals();
    return state;
  });
});

document.querySelectorAll(".tab").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((tab) => tab.classList.remove("active"));
    document.querySelectorAll(".game-mode").forEach((mode) => mode.classList.remove("active"));
    button.classList.add("active");
    $(`#${button.dataset.tab}Game`).classList.add("active");
  });
});

document.querySelectorAll("[data-open-view]").forEach((button) => {
  button.addEventListener("click", () => {
    const view = button.dataset.openView;
    document.querySelector(`.tab[data-tab="${view}"]`)?.click();
    document.querySelector(".games-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
  });
});

document.querySelectorAll("[data-modal]").forEach((button) => {
  button.addEventListener("click", () => openModal(button.dataset.modal));
});

document.querySelectorAll("[data-close-modal]").forEach((button) => {
  button.addEventListener("click", closeModals);
});

document.querySelectorAll(".modal").forEach((modal) => {
  modal.addEventListener("click", (event) => {
    if (event.target === modal) closeModals();
  });
});

function handleTapCoin() {
  tapEffect();
  runAction(elements.tapCoin, () => api("/api/tap", { method: "POST", body: "{}" }));
}

elements.tapCoin.addEventListener("touchstart", (event) => {
  event.preventDefault();
  lastTapCoinTouch = Date.now();
  handleTapCoin();
}, { passive: false });

elements.tapCoin.addEventListener("click", (event) => {
  if (Date.now() - lastTapCoinTouch < 550) {
    event.preventDefault();
    return;
  }
  handleTapCoin();
});

document.addEventListener("dblclick", (event) => event.preventDefault(), { passive: false });
document.addEventListener("gesturestart", (event) => event.preventDefault());
document.addEventListener("gesturechange", (event) => event.preventDefault());
document.addEventListener("gestureend", (event) => event.preventDefault());
document.addEventListener("touchend", (event) => {
  const now = Date.now();
  if (now - lastTouchEnd <= 320) {
    event.preventDefault();
  }
  lastTouchEnd = now;
}, { passive: false });

document.querySelectorAll(".bet").forEach((button) => {
  button.addEventListener("click", () => {
    selectedBet = Number(button.dataset.bet);
    document.querySelectorAll(".bet").forEach((bet) => bet.classList.remove("active"));
    button.classList.add("active");
  });
});

document.querySelectorAll(".launch-bet").forEach((button) => {
  button.addEventListener("click", () => {
    if (launchRound) return;
    selectedLaunchBet = Number(button.dataset.launchBet);
    document.querySelectorAll(".launch-bet").forEach((bet) => bet.classList.remove("active"));
    button.classList.add("active");
  });
});

document.querySelectorAll(".auto-cash").forEach((button) => {
  button.addEventListener("click", () => {
    selectedAutoCashout = Number(button.dataset.autoCashout);
    document.querySelectorAll(".auto-cash").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
  });
});

elements.dropBtn.addEventListener("click", startDropGame);
elements.startLaunch.addEventListener("click", startCoreLaunch);
elements.cashoutLaunch.addEventListener("click", cashoutCoreLaunch);

elements.spinWheel.addEventListener("click", () => {
  elements.wheelResult.className = "wheel-result";
  elements.wheelResult.innerHTML = `<strong>${t("spinWheel")}...</strong><span>${selectedBet}</span>`;
  elements.wheelFace.classList.remove("win-glow");
  clearWheelSelection();
  elements.wheelFace.classList.add("is-spinning");
  tg?.HapticFeedback?.impactOccurred("medium");
  runAction(elements.spinWheel, () => api("/api/roulette", {
    method: "POST",
    body: JSON.stringify({ bet: selectedBet }),
  }));
});

elements.copyRefBtn.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(elements.refLink.textContent);
  } catch {
    // Clipboard may be blocked in some Telegram clients.
  }
  showToast(t("copied"));
});

renderWheel();
applyLanguage();
refresh().finally(() => {
  window.setTimeout(() => elements.loader.classList.add("hide"), 1300);
});
window.setInterval(refresh, 15000);
