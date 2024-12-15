#!/opt/local/bin/julia
# shebang (#!/opt/local/bin/julia) necessary only:
# 1. to execute the script directly from the command line (e.g., ./*.jl) without explicitly calling `julia *.jl`.
#   chmod +x mesh.jl
#   chmod u+x script.sh : only the file owner to execute the script
#   chmod 700 script.sh : read, write, and execute
# 2. or if Julia executable is installed in a specific path (e.g., /opt/local/bin/julia), and you want the script to locate it automatically.

# configure-packages.jl: Install required packages for the project
using Pkg, Dates

# Activate environment
Pkg.activate(".")  # Activates the current directory as the environment

# Start timer
start_time = time( )

# List of required packages
packages = [
    "Meshes",
    "MeshViz",
    "Plots",
    "Sysinfo"  # Ensure correct package names
]

println("Checking and installing packages...\n")

# Helper function to check if a package is already installed
function is_installed( pkg_name )
    dependencies = Pkg.dependencies( )  # Get all dependencies
    return any( x -> x.name == pkg_name, values( dependencies ) )
end

# Install missing packages
for pkg in packages
    print( "Checking for package: $pkg... " )
    if is_installed( pkg )
        println( "already installed." )
    else 
        println( "not found. Installing $pkg..." )
        try
            Pkg.add( pkg )
            println( "$pkg successfully installed." )
        catch e
            println( "Failed to install $pkg. Error: $e" )
        end
    end
end

# End timer
end_time = time( )

# Timestamp
println( "\nGenerated on: ", Dates.format( now( ), "yyyy-mm-dd HH:MM:SS" ) )
println( "Execution time: ", round( end_time - start_time, digits=  2 ), " seconds" )

# dantopa@Xiuhcoatl:util $ ./configure-packages.jl 
#   Activating new project at `~/repos-xiuhcoatl/github/jop/julia/util`
# Checking and installing packages...

# Checking for package: Meshes... not found. Installing Meshes...
#    Resolving package versions...
#     Updating `~/repos-xiuhcoatl/github/jop/julia/util/Project.toml`
#   [eacbb407] + Meshes v0.52.8
#     Updating `~/repos-xiuhcoatl/github/jop/julia/util/Manifest.toml`
#   [621f4979] + AbstractFFTs v1.5.0
#   [1520ce14] + AbstractTrees v0.4.5
#   [79e6a3ab] + Adapt v4.1.1
#   [35492f91] + AdaptivePredicates v1.2.0
#   [66dad0bd] + AliasTables v1.1.3
#   [4fba245c] + ArrayInterface v7.18.0
#   [a9b6321e] + Atomix v1.0.1
#   [0e736298] + Bessels v0.2.8
#   [fa961155] + CEnum v0.5.0
#   [082447d4] + ChainRules v1.72.1
#   [d360d2e6] + ChainRulesCore v1.25.0
#   [7a955b69] + CircularArrays v1.4.0
#   [35d6a980] + ColorSchemes v3.27.1
# ⌅ [3da002f7] + ColorTypes v0.11.5
# ⌃ [c3611d14] + ColorVectorSpace v0.10.0
#   [03fe91ce] + Colorfy v1.1.0
# ⌃ [5ae59095] + Colors v0.12.11
#   [bbf7d656] + CommonSubexpressions v0.3.1
#   [f70d9fcc] + CommonWorldInvalidations v1.0.0
#   [34da2185] + Compat v4.16.0
#   [187b0558] + ConstructionBase v1.5.8
#   [b46f11dc] + CoordRefSystems v0.16.3
#   [9a962f9c] + DataAPI v1.16.0
#   [864edb3b] + DataStructures v0.18.20
#   [e2d170a0] + DataValueInterfaces v1.0.0
#   [927a84f5] + DelaunayTriangulation v1.6.3
#   [163ba53b] + DiffResults v1.1.0
#   [b552c78f] + DiffRules v1.15.1
#   [b4f34e82] + Distances v0.10.12
#   [ffbed154] + DocStringExtensions v0.9.3
#   [4e289a0a] + EnumX v1.0.4
#   [429591f6] + ExactPredicates v2.2.8
#   [1a297f60] + FillArrays v1.13.0
#   [53c48c17] + FixedPointNumbers v0.8.5
#   [f6369f11] + ForwardDiff v0.10.38
#   [0c68f7d7] + GPUArrays v11.1.0
#   [46192b85] + GPUArraysCore v0.2.0
#   [076d061b] + HashArrayMappedTries v0.2.0
#   [7869d1d1] + IRTools v0.4.14
#   [615f187c] + IfElse v0.1.1
#   [d1acc4aa] + IntervalArithmetic v0.22.19
#   [92d709cd] + IrrationalConstants v0.2.2
#   [82899510] + IteratorInterfaceExtensions v1.0.0
#   [692b3bcd] + JLLWrappers v1.6.1
#   [63c18a36] + KernelAbstractions v0.9.31
#   [929cbde3] + LLVM v9.1.3
#   [2ab3a3ac] + LogExpFunctions v0.3.29
#   [1914dd2f] + MacroTools v0.5.13
#   [eacbb407] + Meshes v0.52.8
#   [e1d29d7a] + Missings v1.2.0
#   [77ba4419] + NaNMath v1.0.2
#   [b8a86587] + NearestNeighbors v0.4.21
#   [6fe1bfb0] + OffsetArrays v1.14.2
#   [bac558e1] + OrderedCollections v1.7.0
#   [aea7be01] + PrecompileTools v1.2.1
#   [21216c6a] + Preferences v1.4.3
#   [43287f4e] + PtrArrays v1.2.1
#   [94ee1d12] + Quaternions v0.7.6
#   [c1ae055f] + RealDot v0.1.0
#   [189a3867] + Reexport v1.2.2
#   [ae029012] + Requires v1.3.0
#   [6038ab10] + Rotations v1.7.1
#   [5eaf0fd0] + RoundingEmulator v0.2.1
#   [7e506255] + ScopedValues v1.2.1
#   [a2af1166] + SortingAlgorithms v1.2.1
#   [dc90abb0] + SparseInverseSubset v0.1.2
#   [276daf66] + SpecialFunctions v2.5.0
#   [aedffcd0] + Static v1.1.1
#   [0d7ed370] + StaticArrayInterface v1.8.0
#   [90137ffa] + StaticArrays v1.9.8
#   [1e83bf80] + StaticArraysCore v1.4.3
#   [10745b16] + Statistics v1.11.1
#   [82ae8749] + StatsAPI v1.7.0
#   [2913bbd2] + StatsBase v0.34.4
#   [09ab397b] + StructArrays v0.7.0
#   [3783bdb8] + TableTraits v1.0.1
#   [bd369af6] + Tables v1.12.0
#   [62fd8b95] + TensorCore v0.1.1
#   [06e1c1a7] + TiledIteration v0.5.0
#   [28dd2a49] + TransformsBase v1.6.0
#   [1986cc42] + Unitful v1.21.1
#   [013be700] + UnsafeAtomics v0.3.0
#   [e88e6eb3] + Zygote v0.6.73
#   [700de1a5] + ZygoteRules v0.2.5
#   [4e9b3aee] + CRlibm_jll v1.0.1+0
#   [dad2f222] + LLVMExtra_jll v0.0.34+0
#   [efe28fd5] + OpenSpecFun_jll v0.5.5+0
#   [0dad84c5] + ArgTools v1.1.2
#   [56f22d72] + Artifacts v1.11.0
#   [2a0f44e3] + Base64 v1.11.0
#   [ade2ca70] + Dates v1.11.0
#   [8ba89e20] + Distributed v1.11.0
#   [f43a241f] + Downloads v1.6.0
#   [7b1f6079] + FileWatching v1.11.0
#   [b77e0a4c] + InteractiveUtils v1.11.0
#   [4af54fe1] + LazyArtifacts v1.11.0
#   [b27032c2] + LibCURL v0.6.4
#   [76f85450] + LibGit2 v1.11.0
#   [8f399da3] + Libdl v1.11.0
#   [37e2e46d] + LinearAlgebra v1.11.0
#   [56ddb016] + Logging v1.11.0
#   [d6f4376e] + Markdown v1.11.0
#   [ca575930] + NetworkOptions v1.2.0
#   [44cfe95a] + Pkg v1.11.0
#   [de0858da] + Printf v1.11.0
#   [9a3f8284] + Random v1.11.0
#   [ea8e919c] + SHA v0.7.0
#   [9e88b42a] + Serialization v1.11.0
#   [6462fe0b] + Sockets v1.11.0
#   [2f01184e] + SparseArrays v1.11.0
#   [4607b0f0] + SuiteSparse
#   [fa267f1f] + TOML v1.0.3
#   [a4e569a6] + Tar v1.10.0
#   [cf7118a7] + UUIDs v1.11.0
#   [4ec0a83e] + Unicode v1.11.0
#   [e66e0078] + CompilerSupportLibraries_jll v1.1.1+0
#   [deac9b47] + LibCURL_jll v8.6.0+0
#   [e37daf67] + LibGit2_jll v1.7.2+0
#   [29816b5a] + LibSSH2_jll v1.11.0+1
#   [c8ffd9c3] + MbedTLS_jll v2.28.6+0
#   [14a3606d] + MozillaCACerts_jll v2023.12.12
#   [4536629a] + OpenBLAS_jll v0.3.27+1
#   [05823500] + OpenLibm_jll v0.8.1+2
#   [bea87d4a] + SuiteSparse_jll v7.7.0+0
#   [83775a58] + Zlib_jll v1.2.13+1
#   [8e850b90] + libblastrampoline_jll v5.11.0+0
#   [8e850ede] + nghttp2_jll v1.59.0+0
#   [3f19e933] + p7zip_jll v17.4.0+2
#         Info Packages marked with ⌃ and ⌅ have new versions available. Those with ⌃ may be upgradable, but those with ⌅ are restricted by compatibility constraints from upgrading. To see why use `status --outdated -m`
# Precompiling project...
#   14 dependencies successfully precompiled in 56 seconds. 144 already precompiled.
# Meshes successfully installed.
# Checking for package: MeshViz... not found. Installing MeshViz...
#    Resolving package versions...
#    Installed Distributions ─ v0.25.114
#     Updating `~/repos-xiuhcoatl/github/jop/julia/util/Project.toml`
#   [9ecf9c4f] + MeshViz v0.8.8
# ⌅ [eacbb407] ↓ Meshes v0.52.8 ⇒ v0.32.3
#     Updating `~/repos-xiuhcoatl/github/jop/julia/util/Manifest.toml`
#   [398f06c4] + AbstractLattices v0.3.1
#   [35492f91] - AdaptivePredicates v1.2.0
#   [27a7e980] + Animations v0.4.2
#   [a9b6321e] - Atomix v1.0.1
#   [67c07d97] + Automa v1.1.0
#   [13072b0f] + AxisAlgorithms v1.1.0
#   [39de3d68] + AxisArrays v0.4.7
#   [324d7699] + CategoricalArrays v0.10.8
#   [082447d4] - ChainRules v1.72.1
#   [a2cac450] + ColorBrewer v0.4.0
#   [03fe91ce] - Colorfy v1.1.0
#   [861a8166] + Combinatorics v1.0.2
#   [f70d9fcc] - CommonWorldInvalidations v1.0.0
#   [d38c429a] + Contour v0.6.3
#   [b46f11dc] - CoordRefSystems v0.16.3
#   [a8cc5b0e] + Crayons v4.1.1
# ⌅ [927a84f5] ↓ DelaunayTriangulation v1.6.3 ⇒ v0.8.12
#   [31c24e10] + Distributions v0.25.114
#   [411431e0] + Extents v0.1.4
#   [7a1cc6ca] + FFTW v1.8.0
#   [5789e2e9] + FileIO v1.16.6
#   [6a86dc24] + FiniteDiff v2.26.2
#   [59287772] + Formatting v0.4.3
#   [b38be410] + FreeType v4.1.1
#   [663a7486] + FreeTypeAbstraction v0.10.6
#   [0c68f7d7] - GPUArrays v11.1.0
#   [46192b85] - GPUArraysCore v0.2.0
#   [68eda718] + GeoFormatTypes v0.4.2
#   [cf35fbd7] + GeoInterface v1.4.0
# ⌅ [5c1252a2] + GeometryBasics v0.4.11
# ⌅ [3955a311] + GridLayoutBase v0.9.2
#   [42e2da0e] + Grisu v1.0.2
#   [076d061b] - HashArrayMappedTries v0.2.0
#   [34004b35] + HypergeometricFunctions v0.3.25
#   [7869d1d1] - IRTools v0.4.14
#   [615f187c] - IfElse v0.1.1
#   [2803e5a7] + ImageAxes v0.6.12
#   [c817782e] + ImageBase v0.1.7
#   [a09fc81d] + ImageCore v0.10.5
#   [82e4d734] + ImageIO v0.6.9
#   [bc367c6b] + ImageMetadata v0.9.10
#   [9b13fd28] + IndirectArrays v1.0.0
#   [d25df0c9] + Inflate v0.1.5
#   [18e54dd8] + IntegerMathUtils v0.1.2
#   [a98d9a8b] + Interpolations v0.15.1
#   [8197267c] + IntervalSets v0.7.10
#   [f1662d9f] + Isoband v0.1.1
#   [c8e1da08] + IterTools v1.10.0
#   [682c06a0] + JSON v0.21.4
#   [b835a17e] + JpegTurbo v0.1.5
#   [63c18a36] - KernelAbstractions v0.9.31
#   [5ab0869b] + KernelDensity v0.6.9
#   [929cbde3] - LLVM v9.1.3
#   [b964fa9f] + LaTeXStrings v1.4.0
#   [8cdb02fc] + LazyModules v0.3.1
#   [9c8b4983] + LightXML v0.9.1
#   [d3d80556] + LineSearches v7.3.0
#   [9b3f67b0] + LinearAlgebraX v0.2.10
# ⌅ [ee78f7c6] + Makie v0.19.12
# ⌅ [20f20a25] + MakieCore v0.6.9
#   [dbb5928d] + MappedArrays v0.4.2
# ⌅ [0a4f8689] + MathTeXEngine v0.5.7
#   [9ecf9c4f] + MeshViz v0.8.8
# ⌅ [eacbb407] ↓ Meshes v0.52.8 ⇒ v0.32.3
#   [7475f97c] + Mods v2.2.6
#   [e94cdb99] + MosaicViews v0.3.4
#   [3b2b4ff1] + Multisets v0.4.5
#   [d41bc354] + NLSolversBase v7.8.3
#   [f09324ee] + Netpbm v1.1.1
#   [510215fc] + Observables v0.5.5
#   [52e1d378] + OpenEXR v0.3.3
#   [429524aa] + Optim v1.10.0
#   [90014a1f] + PDMats v0.11.31
#   [f57f5aa1] + PNGFiles v0.4.3
#   [19eb6ba3] + Packing v0.5.1
#   [5432bcbf] + PaddedViews v0.5.12
#   [d96e819e] + Parameters v0.12.3
#   [69de0a69] + Parsers v2.8.1
#   [2ae35dd2] + Permutations v0.4.22
#   [3bbf5609] + PikaParser v0.6.1
#   [eebad327] + PkgVersion v0.3.3
#   [995b91a9] + PlotUtils v1.4.3
#   [647866c9] + PolygonOps v0.1.2
#   [f27b6e38] + Polynomials v4.0.12
#   [85a6dd25] + PositiveFactorizations v0.2.4
#   [08abe8d2] + PrettyTables v2.4.0
#   [27ebfcd6] + Primes v0.5.6
#   [92933f4c] + ProgressMeter v1.10.2
#   [4b34888f] + QOI v1.0.1
#   [1fd47b50] + QuadGK v2.11.1
#   [b3c3ace0] + RangeArrays v0.3.2
#   [c84ed2f1] + Ratios v0.4.5
#   [3cdcf5f2] + RecipesBase v1.3.4
#   [05181044] + RelocatableFolders v1.0.1
#   [286e9d63] + RingLists v0.2.9
#   [79098fc4] + Rmath v0.8.0
#   [fdea26ae] + SIMD v3.7.0
#   [321657f4] + ScientificTypes v3.0.2
#   [30f210dd] + ScientificTypesBase v3.0.0
#   [7e506255] - ScopedValues v1.2.1
#   [6c6a2e73] + Scratch v1.2.1
#   [efcf1570] + Setfield v1.1.1
# ⌅ [65257c39] + ShaderAbstractions v0.4.1
#   [992d4aef] + Showoff v1.0.3
#   [73760f76] + SignedDistanceFields v0.4.0
#   [55797a34] + SimpleGraphs v0.8.6
#   [ec83eff0] + SimplePartitions v0.3.3
#   [cc47b68c] + SimplePolynomials v0.2.18
#   [a6525b86] + SimpleRandom v0.3.2
#   [699a6c99] + SimpleTraits v0.9.4
#   [45858cf5] + Sixel v0.1.3
#   [dc90abb0] - SparseInverseSubset v0.1.2
# ⌅ [c5dd0088] + StableHashTraits v1.3.4
#   [860ef19b] + StableRNGs v1.0.2
#   [cae243ae] + StackViews v0.1.1
#   [aedffcd0] - Static v1.1.1
#   [0d7ed370] - StaticArrayInterface v1.8.0
#   [64bff920] + StatisticalTraits v3.4.0
#   [4c63d2b9] + StatsFuns v1.3.2
#   [892a3eda] + StringManipulation v0.4.0
# ⌅ [09ab397b] ↓ StructArrays v0.7.0 ⇒ v0.6.21
#   [856f2bd8] + StructTypes v1.11.0
#   [731e570b] + TiffImages v0.11.1
#   [06e1c1a7] - TiledIteration v0.5.0
#   [3bb67fe8] + TranscodingStreams v0.11.3
#   [981d1d27] + TriplotBase v0.1.0
#   [9d95972d] + TupleTools v1.6.0
#   [3a884ed6] + UnPack v1.0.2
#   [1cfade01] + UnicodeFun v0.4.1
#   [013be700] - UnsafeAtomics v0.3.0
#   [ecbed89c] + WeakKeyIdDicts v0.1.0
#   [e3aaa7dc] + WebP v0.1.3
#   [efce3f68] + WoodburyMatrices v1.0.0
#   [e88e6eb3] - Zygote v0.6.73
#   [700de1a5] - ZygoteRules v0.2.5
#   [6e34b625] + Bzip2_jll v1.0.8+2
#   [83423d85] + Cairo_jll v1.18.2+1
#   [5ae413db] + EarCut_jll v2.2.4+0
#   [2e619515] + Expat_jll v2.6.4+1
#   [b22a6f82] + FFMPEG_jll v6.1.2+0
#   [f5851436] + FFTW_jll v3.3.10+1
#   [a3f928ae] + Fontconfig_jll v2.15.0+0
#   [d7e528f0] + FreeType2_jll v2.13.3+1
#   [559328eb] + FriBidi_jll v1.0.14+0
#   [78b55507] + Gettext_jll v0.21.0+0
#   [59f7168a] + Giflib_jll v5.2.2+0
#   [7746bdde] + Glib_jll v2.82.2+1
#   [3b182d85] + Graphite2_jll v1.3.14+1
#   [2e76f6c2] + HarfBuzz_jll v8.5.0+0
#   [905a6f67] + Imath_jll v3.1.11+0
#   [1d5cc7b8] + IntelOpenMP_jll v2024.2.1+0
#   [aacddb02] + JpegTurbo_jll v3.0.4+0
#   [c1c5ebd0] + LAME_jll v3.100.2+0
#   [88015f11] + LERC_jll v4.0.0+0
#   [dad2f222] - LLVMExtra_jll v0.0.34+0
#   [1d63c593] + LLVMOpenMP_jll v18.1.7+0
#   [dd4b983a] + LZO_jll v2.10.2+1
# ⌅ [e9f186c6] + Libffi_jll v3.2.2+1
#   [d4300ac3] + Libgcrypt_jll v1.11.0+0
#   [7e76a0d4] + Libglvnd_jll v1.7.0+0
#   [7add5ba3] + Libgpg_error_jll v1.50.0+0
#   [94ce4f54] + Libiconv_jll v1.17.0+1
#   [4b2f31a3] + Libmount_jll v2.40.2+0
#   [89763e89] + Libtiff_jll v4.7.0+0
#   [38a345b3] + Libuuid_jll v2.40.2+0
#   [856f044c] + MKL_jll v2024.2.0+0
#   [e7412a2a] + Ogg_jll v1.3.5+1
#   [18a262bb] + OpenEXR_jll v3.2.4+0
#   [458c3c95] + OpenSSL_jll v3.0.15+1
#   [91d4177d] + Opus_jll v1.3.3+0
# ⌅ [30392449] + Pixman_jll v0.43.4+0
#   [f50d1b31] + Rmath_jll v0.5.1+0
#   [02c8fc9c] + XML2_jll v2.13.5+0
#   [aed1982a] + XSLT_jll v1.1.42+0
#   [ffd25f8a] + XZ_jll v5.6.3+0
#   [4f6342f7] + Xorg_libX11_jll v1.8.6+1
#   [0c0b7dd1] + Xorg_libXau_jll v1.0.11+1
#   [a3789734] + Xorg_libXdmcp_jll v1.1.4+1
#   [1082639a] + Xorg_libXext_jll v1.3.6+1
#   [ea2f1a96] + Xorg_libXrender_jll v0.9.11+1
#   [14d82f49] + Xorg_libpthread_stubs_jll v0.1.1+1
#   [c7cfdc94] + Xorg_libxcb_jll v1.17.0+1
#   [c5fb5394] + Xorg_xtrans_jll v1.5.0+1
#   [3161d3a3] + Zstd_jll v1.5.6+1
#   [9a68df92] + isoband_jll v0.2.3+0
#   [a4ae2306] + libaom_jll v3.9.0+0
#   [0ac62f75] + libass_jll v0.15.2+0
#   [f638f0a6] + libfdk_aac_jll v2.0.3+0
#   [b53b4c65] + libpng_jll v1.6.44+0
#   [075b6546] + libsixel_jll v1.10.3+1
#   [f27f6e37] + libvorbis_jll v1.3.7+2
#   [c5f90fcd] + libwebp_jll v1.4.0+0
#   [1317d2d5] + oneTBB_jll v2021.12.0+0
#   [1270edf5] + x264_jll v10164.0.0+0
# ⌅ [dfaa095f] + x265_jll v3.6.0+0
#   [8bf52ea8] + CRC32c v1.11.0
#   [9fa8497b] + Future v1.11.0
#   [a63ad114] + Mmap v1.11.0
#   [3fa0cd96] + REPL v1.11.0
#   [1a1011a3] + SharedArrays v1.11.0
#   [f489334b] + StyledStrings v1.11.0
#   [8dfed614] + Test v1.11.0
#   [efcefdf7] + PCRE2_jll v10.42.0+1
#         Info Packages marked with ⌅ have new versions available but compatibility constraints restrict them from upgrading. To see why use `status --outdated -m`
# Precompiling project...
#   13 dependencies successfully precompiled in 111 seconds. 313 already precompiled.
# MeshViz successfully installed.
# Checking for package: Plots... not found. Installing Plots...
#    Resolving package versions...
#     Updating `~/repos-xiuhcoatl/github/jop/julia/util/Project.toml`
#   [91a5bcdd] + Plots v1.40.9
#     Updating `~/repos-xiuhcoatl/github/jop/julia/util/Manifest.toml`
#   [d1d4a3ce] + BitFlags v0.1.9
#   [944b1d66] + CodecZlib v0.7.6
#   [f0e56b4a] + ConcurrentUtilities v2.4.3
#   [8bb1440f] + DelimitedFiles v1.9.1
#   [460bff9d] + ExceptionUnwrapping v0.1.11
#   [c87230d0] + FFMPEG v0.4.2
#   [1fa38f19] + Format v1.3.7
#   [28b8d3ca] + GR v0.73.9
#   [cd3eb016] + HTTP v1.10.14
#   [1019f520] + JLFzf v0.1.9
#   [23fbe1c1] + Latexify v0.16.5
#   [e6f89c97] + LoggingExtras v1.1.0
#   [739be429] + MbedTLS v1.1.9
#   [442fdcdd] + Measures v0.3.2
#   [4d8831e6] + OpenSSL v1.4.3
#   [b98c9c47] + Pipe v1.3.0
#   [ccf2f8ad] + PlotThemes v3.3.0
#   [91a5bcdd] + Plots v1.40.9
#   [01d81517] + RecipesPipeline v0.6.12
#   [777ac1f9] + SimpleBufferStream v1.2.0
#   [5c2747f8] + URIs v1.5.1
#   [45397f5d] + UnitfulLatexify v1.6.4
#   [41fe7b60] + Unzip v0.2.0
#   [ee1fde0b] + Dbus_jll v1.14.10+0
#   [2702e6a9] + EpollShim_jll v0.0.20230411+1
# ⌅ [b22a6f82] ↓ FFMPEG_jll v6.1.2+0 ⇒ v4.4.4+1
#   [0656b61e] + GLFW_jll v3.4.0+1
#   [d2c73de3] + GR_jll v0.73.9+0
#   [36c8627f] + Pango_jll v1.54.1+0
#   [c0090381] + Qt6Base_jll v6.7.1+1
#   [629bc702] + Qt6Declarative_jll v6.7.1+2
#   [ce943373] + Qt6ShaderTools_jll v6.7.1+1
#   [e99dba38] + Qt6Wayland_jll v6.7.1+1
#   [a44049a8] + Vulkan_Loader_jll v1.3.243+0
#   [a2964d1f] + Wayland_jll v1.21.0+1
#   [2381bf8a] + Wayland_protocols_jll v1.31.0+0
#   [f67eecfb] + Xorg_libICE_jll v1.1.1+0
#   [c834827a] + Xorg_libSM_jll v1.2.4+0
#   [935fb764] + Xorg_libXcursor_jll v1.2.0+4
#   [d091e8ba] + Xorg_libXfixes_jll v5.0.3+4
#   [a51aa0fd] + Xorg_libXi_jll v1.7.10+4
#   [d1454406] + Xorg_libXinerama_jll v1.1.5+0
#   [ec84b674] + Xorg_libXrandr_jll v1.5.4+0
#   [cc61e674] + Xorg_libxkbfile_jll v1.1.2+1
#   [e920d4aa] + Xorg_xcb_util_cursor_jll v0.1.4+0
#   [12413925] + Xorg_xcb_util_image_jll v0.4.0+1
#   [2def613f] + Xorg_xcb_util_jll v0.4.0+1
#   [975044d2] + Xorg_xcb_util_keysyms_jll v0.4.0+1
#   [0d47668e] + Xorg_xcb_util_renderutil_jll v0.3.9+1
#   [c22f9ab0] + Xorg_xcb_util_wm_jll v0.4.1+1
#   [35661453] + Xorg_xkbcomp_jll v1.4.6+1
#   [33bec58e] + Xorg_xkeyboard_config_jll v2.39.0+0
#   [35ca27e7] + eudev_jll v3.2.9+0
#   [214eeab7] + fzf_jll v0.56.3+0
#   [1a1c6b14] + gperf_jll v3.1.1+1
#   [1183f4f0] + libdecor_jll v0.2.2+0
#   [2db6ffa8] + libevdev_jll v1.11.0+0
#   [36db933b] + libinput_jll v1.18.0+0
#   [009596ad] + mtdev_jll v1.1.6+0
# ⌅ [1270edf5] ↓ x264_jll v10164.0.0+0 ⇒ v2021.5.5+0
# ⌅ [dfaa095f] ↓ x265_jll v3.6.0+0 ⇒ v3.5.0+0
#   [d8fb68d0] + xkbcommon_jll v1.4.1+1
#         Info Packages marked with ⌅ have new versions available but compatibility constraints restrict them from upgrading. To see why use `status --outdated -m`
# Precompiling project...
#   2 dependencies successfully precompiled in 96 seconds. 388 already precompiled.
# Plots successfully installed.
# Checking for package: Sysinfo... not found. Installing Sysinfo...
# Failed to install Sysinfo. Error: Pkg.Types.PkgError("The following package names could not be resolved:\n * Sysinfo (not found in project, manifest or registry)\n\e[36m   Suggestions:\e[39m \e[0m\e[1mS\e[22m\e[0m\e[1my\e[22m\e[0m\e[1ms\e[22m\e[0m\e[1mI\e[22m\e[0m\e[1mn\e[22m\e[0m\e[1mf\e[22m\e[0m\e[1mo\e[22m")

# Generated on: 2024-12-14 19:34:57
# Execution time: 276.15 seconds

