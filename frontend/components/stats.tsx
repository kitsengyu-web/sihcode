"use client";

const Stats2 = () => {
  return (
    <section className="py-32">
      <div className="container">
        <div className="grid gap-8 md:grid-cols-3">
          <div className="grid gap-4 md:col-span-3 lg:grid-cols-3">
            <div className="bg-black flex h-60 flex-col justify-between rounded-lg p-6">
              <div className="mb-4">
                <p className="text-muted-foreground text-sm">
                  Streamlined design workflows
                </p>
              </div>
              <div>
                <h3 className="text-6xl font-semibold text-white">82%</h3>
                <p className="text-foreground/80 text-base">
                  of manual design tasks eliminated
                </p>
              </div>
            </div>

            <div className="bg-black flex h-60 flex-col justify-between rounded-lg p-6">
              <div className="mb-4">
                <p className="text-muted-foreground text-sm">
                  Design precision
                </p>
              </div>
              <div>
                <h3 className="text-6xl font-semibold text-white">99.9%</h3>
                <p className="text-foreground/80 text-base">
                  design consistency achieved
                </p>
              </div>
            </div>

            <div className="bg-black flex h-60 flex-col justify-between rounded-lg p-6">
              <div className="mb-4">
                <p className="text-muted-foreground text-sm">
                  Scalable design projects
                </p>
              </div>
              <div>
                <h3 className="text-6xl font-semibold text-white">520K+</h3>
                <p className="text-foreground/80 text-base">
                  total design assets created
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export { Stats2 };
