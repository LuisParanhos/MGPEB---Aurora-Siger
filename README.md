# MGPEB — Aurora Siger
Módulo de Gerenciamento de Pouso e Estabilização de Base Marciana

---

## Sobre o Projeto

O projeto foi desenvolvido para simular um sistema de controle de pouso de módulos de uma base em Marte, a principal ideia é praticar estruturas de dados como insertion sort, buscas, filas e pilhas.

---

## Como Executar

Precisa ter Python 3.8 ou superior.
Não utilizei nenhuma biblioteca externa, apenas usamos a `random` para dados aleatórios.

```bash
python mgpeb.py
```

---

## O que o Sistema Faz

O programa roda sempre em sequência passando por algumas etapas na execução:

**1. Geração da fila**

São criados alguns módulos no início com características aleatórias como combustível, prioridade, sensores etc.
Garanti apenas que exista pelo menos um módulo de cada tipo para evitar cenários inválidos durante a execução.

Resultado do código:

<img width="620" height="292" alt="image" src="https://github.com/user-attachments/assets/492b6981-1f0f-4dae-a766-355ad8682470" />


**2. Buscas na filas**

O sistema faz algumas buscas simples como:

- Módulo com menor combustível
- Módulo com maior prioridade
- Módulo de um tipo específico

Parte para exercitar busca em listas.

Resultado do código:

<img width="624" height="208" alt="image" src="https://github.com/user-attachments/assets/404b03b3-eaa9-435d-92ff-a30cdfd6181d" />


**3. Ordenação da fila**

A fila é reorganizada usando o Insertion Sort, escolhi o algoritmo pois o número de dados utilizado é pequeno.

Critério de ordenação:

- Baseado na prioridade de cada módulo
- Em caso da prioridade ser igual, o que tiver menos combustível vai primeiro

Resultado da etapa:

<img width="624" height="208" alt="image" src="https://github.com/user-attachments/assets/aa9dda1c-9f37-4f4e-8555-318824a21273" />

**4. Processo de pouso**

Nessa etapa cada módulo é analisado individualmente verificando os seguintes parâmetros:

- Combustível
- Sensores
- Condições atmosféricas
- Disponibilidade da pista

Caso tudo esteja ok, o módulo recebe a autorização para pousar. Caso seja uma emergência (quando o combustível estiver muito baixo) e a criticidade for alta, ele ainda pode pousar se as outras condições forem verdadeiras.

Resultado do código:

<img width="518" height="625" alt="image" src="https://github.com/user-attachments/assets/6cb2a52e-f924-4cc7-852a-f64f7874b4ab" />


**5. Resultado Final**

No final da execução o programa separa os seguintes pontos: módulos que pousaram com sucesso e módulos bloqueados.

Resultado do código:

<img width="668" height="490" alt="image" src="https://github.com/user-attachments/assets/e4846e06-87ac-4c7d-bef5-e3513f5b2d8f" />


**6. Alertas**

Os bloqueios geram mensagens que são armazenadas e exibidas no final, do mais recente para o mais antigo.

---

## Regras de Autorização

Um módulo só pode pousar normalmente se:

- Combustível > 15%
- Sensores funcionando
- Pista disponível
- Vento abaixo de 80 km/h e sem tempestade

### Pouso de emergência

Se o combustível estiver abaixo do mínimo, mas a criticidade for muito alta (≥ 9), o pouso ainda pode ser permitido — desde que o resto esteja ok.

---

## Simulação da Descida

A descida é simulada de forma simplificada em duas fases:

- Fase balística (queda livre com gravidade de Marte)
- Fase com retrofoguetes

Quando o módulo atinge cerca de 600m de altitude, os retrofoguetes são ativados e a queda passa a ser controlada.

Exemplo de saída:

```
    --- Descida de [HAB-01] ---
    h0=9687m  v0=67m/s  tRetro=55s
    0s    9687m   Balística
    13s   8501m   Balística
    >>> retrofoguetes ativados
    55s   600m    Controlado
    Pouso estimado: ~243s
```

---

## Estruturas de Dados Usadas

Usei basicamente listas do Python:

```python
fila.pop(0)        # módulos aguardando análise
pousados.append()  # módulos que pousaram
alertas.pop()      # controle de alertas
```


---



