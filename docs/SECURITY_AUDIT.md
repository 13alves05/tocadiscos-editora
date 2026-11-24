# Security Audit Standard

> Checklist reutilizável para este repositório. Não é um certificado de teste de intrusão, parecer jurídico ou garantia de segurança.
>
> Contexto inicial (confirmar sempre no código atual): Python CLI, CSV, gestão de autores/álbuns/músicas, relatórios financeiros, pesquisa, áudio, administração local e histórico/reversão.

## Regras de execução
- Registar branch, commit, estado do working tree e ambiente antes de começar.
- Trabalho local e isolado. Não fazer deploy, merge, migrações de produção, alterações em painéis de fornecedores, rotação de credenciais, reescrita do histórico Git ou contacto com utilizadores.
- Não usar dados, contas ou pagamentos reais. Não imprimir nem commitar valores secretos.
- Não instalar dependências nem executar comandos destrutivos sem aprovação. Preservar alterações existentes.
- Corrigir apenas vulnerabilidades confirmadas, em alterações pequenas, com teste de regressão. Um teste deve demonstrar a falha antes e passar depois, sempre que seja seguro executá-lo.
- Parar e pedir aprovação se a correção exigir acesso de produção, alteração de dados, rotação de segredos ou mudança material de autenticação/pagamentos.

## Descoberta obrigatória
Antes de testar, entregar: (1) resumo de arquitetura em cinco linhas; (2) inventário de rotas/API, server actions, jobs, CLI, deep links, uploads e interfaces administrativas existentes; (3) autenticação, autorização, validação e ownership por ponto de entrada; (4) dados sensíveis, papéis, segredos, integrações e operações irreversíveis; (5) comandos existentes de testes, lint, typecheck, build e scanners. Não inventar funcionalidades. Ausência comprovada = Não aplicável; falta de prova = Validação manual necessária.

## As 14 verificações
Para cada uma indicar estado (Seguro com evidência / Vulnerável / Não aplicável com evidência / Validação manual necessária), gravidade, impacto, ficheiro/linha, prova, correção e teste.

1. **Autorização/admin (CWE-862):** validar no servidor permissões em cada rota, página, ação, job e comando privilegiado. UI escondida não é controlo de acesso.
2. **IDOR/ownership (CWE-639):** alterar IDs para testar acesso a dados de terceiros; impor ownership e tenant scope em leituras, escritas e eliminações; testar RLS quando exista.
3. **Segredos no cliente (CWE-798):** inspecionar bundles, pacotes mobile, source maps e variáveis públicas. Chaves privilegiadas/service-role nunca podem chegar ao cliente.
4. **Preços/totais (CWE-472):** se houver comércio/créditos, calcular preços, descontos, impostos e totais no servidor; nunca confiar no cliente.
5. **Validação (CWE-20):** validar tipo, formato, tamanho, intervalo, enum, nulabilidade e regras de negócio em todas as fronteiras.
6. **Pagamentos (CWE-345):** se existirem, validar assinatura do webhook, ambiente, evento, encomenda, valor e moeda; garantir idempotência. Redirect do browser não confirma pagamento.
7. **Concorrência (CWE-362):** proteger stock, cupões, saldos, convites, quotas e ações únicas com transações, updates atómicos, constraints ou locks; testar concorrência.
8. **Mass assignment (CWE-915):** allowlist de campos editáveis; nunca aceitar do cliente role, permissões, owner, plano, saldo ou estado de verificação.
9. **Brute force (CWE-307):** rever login, PIN, OTP, reset e recuperação para rate limits, atrasos progressivos e mensagens seguras.
10. **Prompt injection (OWASP LLM01):** se houver IA, tratar prompts/documentos como não confiáveis; IA não concede permissões nem decide dinheiro; limitar ferramentas e exigir confirmação para ações consequentes.
11. **XSS (CWE-79):** rever HTML, Markdown, rich text, URLs e DOM sinks; conteúdo do utilizador é texto por omissão; sanitizar HTML apenas quando necessário; rever CSP/cookies.
12. **Uploads (CWE-434):** se existirem, validar conteúdo real, extensão e tamanho; nome gerado, armazenamento seguro e autorização; bloquear HTML/SVG salvo suporte seguro explícito.
13. **Segredos no Git (CWE-540):** inspecionar ficheiros versionados, ignore rules, logs e histórico com scanners existentes. Não reescrever histórico nem rodar credenciais sem aprovação; tratar segredos expostos como comprometidos.
14. **SQL/injeção (CWE-89):** queries parametrizadas/ORM seguro; rever SQL raw, identificadores dinâmicos, filtros, shell e caminhos; allowlist para identificadores.

## Verificações adicionais conforme a aplicação
- **Web/API:** CSRF para sessões cookie, CORS allowlist, cookies seguros, expiração/rotação de sessão, headers, redirects, fuga de erros, cache e rate limits.
- **Mobile/PWA:** armazenamento local e chaves, backups, deep links, WebViews, permissões, TLS, logs, clipboard/screenshots e cache offline.
- **BaaS/DB:** RLS testada com duas identidades reais de teste; privilégio mínimo; migrations revistas. Mocks não provam políticas do fornecedor.
- **CLI/desktop:** path traversal, desserialização, execução de comandos, credenciais locais, permissões e integridade de backups.
- **IA/workflows:** scopes OAuth mínimos, isolamento de tokens, assinatura de webhooks, SSRF, limites, redação de segredos e aprovações.
- **Site estático:** confirmar ausência de backend/chaves privilegiadas no build; rever formulários, links externos, analytics, dependências, headers e deployment.

## Testes e relatório
- Começar por inspeção read-only e comandos existentes. Executar primeiro testes focados e depois suite, lint, typecheck, build e scanners disponíveis.
- Usar dados locais isolados. Para autorização/RLS, testar duas identidades; mocks não provam RLS real.
- Registar comandos e resultados reais. Não alegar validação em produção, painéis externos, dispositivos reais ou pagamentos reais sem os ter testado.
- Commit por correção apenas se o workflow o permitir, com mensagem security: <issue>; caso contrário, deixar alterações sem commit.
- Relatório final: arquitetura; inventário de pontos de entrada; tabela dos 14 pontos com estado/gravidade/evidência/impacto/correção/teste; achados adicionais; comandos e resultados; ações manuais pendentes; limitações; até cinco testes manuais prioritários.

## Instrução para Claude Code / agente
Audita este repositório real usando este documento. Mapeia primeiro arquitetura e pontos de entrada. Avalia os 14 pontos e as verificações adicionais aplicáveis. Cita ficheiros e linhas. Não marques Seguro sem prova no código nem Não aplicável sem justificação. Corrige apenas vulnerabilidades confirmadas, uma de cada vez, com teste de regressão. Mantém tudo local e isolado. Não faças deploy, não toques em produção, não alteres painéis, não rodes segredos, não reescrevas histórico, não instales dependências nem alteres fluxos de autenticação/pagamento/produto sem aprovação explícita. Se não for possível provar um controlo localmente, marca Validação manual necessária e explica exatamente o que falta. Termina com o relatório acima.

## Referências
- OWASP ASVS v5.0.0 (baseline estável): https://asvs.owasp.org/
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/

Esta checklist não demonstra, por si só, conformidade ASVS.
