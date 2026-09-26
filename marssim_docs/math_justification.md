# Mathematical & Architectural Justification

The conclusion that the architecture transitions from *memory-bound* to *compute-bound and thermal-bound*, necessitating a reduction in SRAM, is derived from first-principles computer architecture scaling laws applied to the parameters provided in the prompt.

## 1. The Transition to Compute-Bound (Breaking the Memory Wall)

**The Decode Phase Bottleneck (Autoregressive Generation)**
In LLM inference, generating a new token requires loading the *entire* model weights and the KV cache from memory to the compute units (Tensor Cores) for every single step.

*   **Baseline (Shoreline HBM)**: Modern HBM3e provides roughly 8 TB/s of bandwidth. For a massive LLM, the GPU can compute the matrix-vector multiplication much faster than 8 TB/s can feed the weights. Therefore, the compute units sit idle waiting for data. This is the definition of being **memory-bandwidth bound**.
*   **Custom Design (Stacked DRAM + 1000x BW)**: The prompt specifies a **1000x increase in bandwidth**. 
    *   $8 \text{ TB/s} * 1000 = 8,000 \text{ TB/s}$ (or 8 Petabytes per second).
    *   With 8,000 TB/s, the weights and KV cache can be delivered to the Tensor Cores almost instantaneously. The time taken to move data becomes negligible compared to the time taken to actually perform the mathematical operations (FLOPs).
    *   Consequently, the Tensor Cores are now running at 100% capacity and cannot go any faster, making the system strictly **compute-bound**. 

## 2. The Reallocation of Die Space (SRAM to Compute)

**Why do modern GPUs have massive SRAM caches?**
GPUs feature large on-die L2/L3 SRAM caches primarily to hide the latency and bandwidth limitations of off-chip memory (HBM/GDDR). Caching frequently used data prevents the system from having to pay the "penalty" of fetching from slower HBM.

**The Impact of 1000x Bandwidth via TSVs**
*   With 3D Stacked DRAM connected by thousands of Through-Silicon Vias (TSVs), the DRAM is located microns away from the compute die vertically.
*   Because the bandwidth is 1000x higher, the "penalty" for fetching from DRAM is essentially eradicated. The stacked DRAM behaves almost like a massive, slightly slower L3 cache.
*   Therefore, dedicating huge amounts of precious 2D die area to SRAM becomes redundant and mathematically inefficient.
*   **The Architectural Pivot**: To maximize performance in a now compute-bound system, chip designers would remove the large SRAM blocks and fill that reclaimed silicon real estate with more ALUs and Tensor Cores, directly increasing the theoretical peak FLOPs.

## 3. The Transition to Thermal-Bound

**The Power Density Problem**
*   **Baseline (2.5D Packaging)**: The GPU die and the HBM stacks sit side-by-side on an interposer. Heat is dissipated across a wide 2D surface area.
*   **Custom Design (3D Stacking)**: The DRAM is stacked *directly on top* of the GPU compute die.
    *   DRAM generates heat. The GPU generates massive heat.
    *   Because the DRAM acts as a thermal blanket over the GPU, it is significantly harder to cool the bottom compute layer.
    *   Furthermore, utilizing 1000+ TSVs constantly pushing data at 1000x bandwidth generates immense concentrated power draw.
*   **The Result**: The architecture becomes bottlenecked by how fast heat can be removed (thermal-bound). To prevent melting, the system must employ "dark silicon" (powering down unused sections of the chip) or run at lower overall clock frequencies, relying on the massive data width to maintain high throughput despite a slower clock.
